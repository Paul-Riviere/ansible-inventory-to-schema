import click
from ansible_inventory_to_schema.__version__ import __version__
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
@click.option('-i','--inventory-path', default='.', show_default=True)
def generate(inventory_path):
    click.echo("Inventory path: " + inventory_path)
    dl = DataLoader()
    im = InventoryManager(loader=dl, sources=[inventory_path])
    click.echo(im.get_hosts())


cli.add_command(generate)
