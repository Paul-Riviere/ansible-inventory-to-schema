import click
from ansible_inventory_to_schema.__version__ import __version__
from ansible_inventory_to_schema.commands.generate import Generate


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
@click.option('-i', '--inventory-path', default='.', show_default=True)
def generate(inventory_path):
    Generate.run(inventory_path)


cli.add_command(generate)
