from primitive.utils.actions import BaseAction
from loguru import logger
from primitive.__about__ import __version__
from ..utils.exceptions import P_CLI_100
import sys
import psutil
from ..db import sqlite
from ..db.models import JobRun
from time import sleep


class Monitor(BaseAction):
    def start(self):
        logger.remove()
        logger.add(
            sink=sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            backtrace=True,
            diagnose=True,
            level="DEBUG" if self.primitive.DEBUG else "INFO",
        )
        logger.info("[*] primitive monitor")
        logger.info(f"[*] Version: {__version__}")

        # Initialize the database
        sqlite.init()

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
            while True:
                logger.debug("Syncing children...")
                self.primitive.hardware._sync_children()

                # Look for entries in the database
                procs = JobRun.objects.all()

                # No procs in the database => nothing to monitor
                if len(procs) == 0:
                    sleep_amount = 5
                    logger.debug(
                        f"No active processes found... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                # If there is a process in the database, take over check in from agent
                try:
                    self.primitive.hardware.check_in_http(is_online=True)
                except Exception as exception:
                    logger.exception(f"Error checking in hardware: {exception}")

                # For each process, check status and kill if cancelled
                for proc in procs:
                    logger.debug(f"Checking process {proc.pid}...")

                    status = self.primitive.jobs.get_job_status(proc.job_run_id)
                    status_value = status.data["jobRun"]["status"]
                    conclusion_value = status.data["jobRun"]["conclusion"]

                    logger.debug(f"- Status: {status_value}")
                    logger.debug(f"- Conclusion: {conclusion_value}")

                    try:
                        parent = psutil.Process(proc.pid)
                    except psutil.NoSuchProcess:
                        logger.debug("Process not found")
                        continue

                    children = parent.children(recursive=True)

                    if status_value == "completed" and conclusion_value == "cancelled":
                        logger.warning("Job cancelled by user")
                        for child in children:
                            logger.debug(f"Killing child process {child.pid}...")
                            child.kill()

                        logger.debug(f"Killing parent process {parent.pid}...")
                        parent.kill()

                sleep(5)

        except KeyboardInterrupt:
            logger.info("[*] Stopping primitive monitor...")
            try:
                self.primitive.hardware.check_in_http(
                    is_available=False, is_online=False, stopping_agent=True
                )

            except P_CLI_100 as exception:
                logger.error("[*] Error stopping primitive monitor.")
                logger.error(str(exception))
            sys.exit()
