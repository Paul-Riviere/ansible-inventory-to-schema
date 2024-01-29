import click
from ansible_inventory_to_schema.__version__ import __version__
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
@click.option('-i', '--inventory-path', default='.', show_default=True)
def generate(inventory_path):
    click.echo("Inventory path: " + inventory_path)
    dl = DataLoader()
    im = InventoryManager(loader=dl, sources=[inventory_path])

    count = 0

    plantuml_output_file = open("generated_plantuml", "w")
    plantuml_output_file.write('@startuml\n')

    for group, host_list in im.get_groups_dict().items():
        count += 1
        plantuml_group = 'rectangle "**' + group + '**\n--'.encode("unicode_escape").decode("UTF-8")
        for host in host_list:
            plantuml_group += "\n".encode("unicode_escape").decode("UTF-8") + host

        plantuml_group += '" as rectangle' + str(count) + "\n"
        plantuml_output_file.write(plantuml_group)

    plantuml_output_file.write('@enduml')
    plantuml_output_file.close()


cli.add_command(generate)
