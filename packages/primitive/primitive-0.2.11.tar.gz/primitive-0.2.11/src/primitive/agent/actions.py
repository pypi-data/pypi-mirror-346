import sys
from time import sleep

from loguru import logger

from primitive.__about__ import __version__
from primitive.utils.actions import BaseAction

from .runner import Runner
from .uploader import Uploader
from ..db import sqlite
from ..db.models import JobRun


class Agent(BaseAction):
    def execute(
        self,
    ):
        logger.remove()
        logger.add(
            sink=sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            backtrace=True,
            diagnose=True,
            level="DEBUG" if self.primitive.DEBUG else "INFO",
        )
        logger.info("[*] primitive agent")
        logger.info(f"[*] Version: {__version__}")

        # Initialize the database
        sqlite.init()

        # Create uploader
        uploader = Uploader(primitive=self.primitive)

        # self.primitive.hardware.update_hardware_system_info()
        try:
            # hey stupid:
            # do not set is_available to True here, it will mess up the reservation logic
            # only set is_available after we've checked that no active reservation is present
            # setting is_available of the parent also effects the children,
            # which may have active reservations as well
            self.primitive.hardware.check_in_http(is_online=True)
        except Exception as exception:
            logger.exception(f"Error checking in hardware: {exception}")
            sys.exit(1)

        try:
            active_reservation_id = None
            active_reservation_pk = None

            while True:
                logger.debug("Scanning for files to upload...")
                uploader.scan()

                hardware = self.primitive.hardware.get_own_hardware_details()

                if hardware["activeReservation"]:
                    if (
                        hardware["activeReservation"]["id"] != active_reservation_id
                        or hardware["activeReservation"]["pk"] != active_reservation_pk
                    ):
                        logger.warning("New reservation for this hardware.")
                        active_reservation_id = hardware["activeReservation"]["id"]
                        active_reservation_pk = hardware["activeReservation"]["pk"]
                        logger.debug("Active Reservation:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")

                        logger.debug("Running pre provisioning steps for reservation.")
                        self.primitive.provisioning.add_reservation_authorized_keys(
                            reservation_id=active_reservation_id
                        )
                else:
                    if (
                        hardware["activeReservation"] is None
                        and active_reservation_id is not None
                        # and hardware["isAvailable"] NOTE: this condition was causing the CLI to get into a loop searching for job runs
                    ):
                        logger.debug("Previous Reservation is Complete:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")
                        logger.debug(
                            "Running cleanup provisioning steps for reservation."
                        )
                        self.primitive.provisioning.remove_reservation_authorized_keys(
                            reservation_id=active_reservation_id
                        )
                        active_reservation_id = None
                        active_reservation_pk = None

                if not active_reservation_id:
                    self.primitive.hardware.check_in_http(
                        is_available=True, is_online=True
                    )
                    sleep_amount = 5
                    logger.debug(
                        f"No active reservation found... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                job_runs_result = self.primitive.jobs.get_job_runs(
                    status="pending", first=1, reservation_id=active_reservation_id
                )

                pending_job_runs = [
                    edge["node"] for edge in job_runs_result.data["jobRuns"]["edges"]
                ]

                if not pending_job_runs:
                    self.primitive.hardware.check_in_http(is_online=True)
                    sleep_amount = 5
                    logger.debug(
                        f"Waiting for Job Runs... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                for job_run in pending_job_runs:
                    logger.debug("Found pending Job Run")
                    logger.debug(f"Job Run ID: {job_run['id']}")
                    logger.debug(f"Job Name: {job_run['job']['name']}")

                    JobRun.objects.create(
                        job_run_id=job_run["id"],
                        pid=None,
                    )

                    runner = Runner(
                        primitive=self.primitive,
                        job_run=job_run,
                        max_log_size=500 * 1024,
                    )

                    try:
                        runner.setup()
                    except Exception as exception:
                        logger.exception(
                            f"Exception while initializing runner: {exception}"
                        )
                        self.primitive.jobs.job_run_update(
                            id=job_run["id"],
                            status="request_completed",
                            conclusion="failure",
                        )
                        JobRun.objects.filter_by(job_run_id=job_run["id"]).delete()
                        continue

                    try:
                        runner.execute()
                    except Exception as exception:
                        logger.exception(f"Exception while executing job: {exception}")
                        self.primitive.jobs.job_run_update(
                            id=job_run["id"],
                            status="request_completed",
                            conclusion="failure",
                        )
                    finally:
                        runner.cleanup()

                        # NOTE: also run scan here to force upload of artifacts
                        # This should probably eventually be another daemon?
                        uploader.scan()

                        JobRun.objects.filter_by(job_run_id=job_run["id"]).delete()

                sleep(5)
        except KeyboardInterrupt:
            logger.info("[*] Stopping primitive agent...")
