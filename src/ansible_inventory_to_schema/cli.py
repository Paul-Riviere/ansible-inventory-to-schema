import click
from ansible_inventory_to_schema.__version__ import __version__


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
def generate():
    print("Hello World")


cli.add_command(generate)
