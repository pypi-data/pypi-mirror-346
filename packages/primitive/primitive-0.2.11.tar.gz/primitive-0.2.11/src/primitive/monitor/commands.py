import click
import typing

if typing.TYPE_CHECKING:
    from ..client import Primitive


@click.command("monitor")
@click.pass_context
def cli(context):
    """monitor"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    primitive.monitor.start()
