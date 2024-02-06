import click
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


class Generate:
    @staticmethod
    def run(inventory_path):
        click.echo("Inventory path: " + inventory_path + "\n")
        dl = DataLoader()
        im = InventoryManager(loader=dl, sources=[inventory_path])

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
    def graph_group(group, result={"groups": [], "links": []}):
        for kid in group.child_groups:
            temp_result = Generate.graph_group(kid, result)
            result["groups"] += temp_result["groups"]
            result["links"] += temp_result["links"]

            if group.get_name() != "all":
                result["links"].append(group.get_name() + "-->" + kid.get_name() + "\n")
        
        temp_group = ""
        if group.get_name() != "all":
            temp_group = 'rectangle "**' + group.get_name() + '**\n--'.encode("unicode_escape").decode("UTF-8")
            for host in group.hosts:
                temp_group += "\n".encode("unicode_escape").decode("UTF-8") + host.name

            temp_group += '" as ' + group.get_name() + "\n"
            result["groups"].append(temp_group)
        
        return result
