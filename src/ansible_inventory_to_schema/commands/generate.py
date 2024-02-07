import click
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


class Generate:
    @staticmethod
    def run(inventory_path):
        click.echo("Inventory path: " + inventory_path + "\n")
        dl = DataLoader()
        im = InventoryManager(loader=dl, sources=[inventory_path])

        # print(im.groups["webservers"].hosts)

        result = Generate.graph_group(im.groups["all"])
        formated_result = {"groups": list(dict.fromkeys(result["groups"])), "links": list(dict.fromkeys(result["links"]))}

        with open("generated_plantuml", "w") as plantuml_output_file:
            plantuml_output_file.write('@startuml\n')
            for group in formated_result["groups"]:
                plantuml_output_file.write(group)
            for link in formated_result["links"]:
                plantuml_output_file.write(link)
            plantuml_output_file.write('@enduml')

    @staticmethod
    def graph_group(root_group):
        result = {"groups": set(), "links": set()}
        stack = [root_group]

        while stack:
            current_group = stack.pop()

            if current_group.get_name() != "all":
                temp_group = 'rectangle "**' + current_group.get_name() + '**\n--'.encode("unicode_escape").decode(
                    "UTF-8")
                for host in current_group.hosts:
                    temp_group += "\n".encode("unicode_escape").decode("UTF-8") + host.name
                temp_group += '" as ' + current_group.get_name() + "\n"
                result["groups"].add(temp_group)

            for kid in current_group.child_groups:
                if current_group.get_name() != "all":
                    result["links"].add(current_group.get_name() + "-->" + kid.get_name() + "\n")
                stack.append(kid)

        return result