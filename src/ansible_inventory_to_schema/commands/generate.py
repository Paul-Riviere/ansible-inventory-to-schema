import click
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


class Generate:
    @staticmethod
    def run(inventory_path):
        click.echo("Inventory path: " + inventory_path + "\n")
        dl = DataLoader()
        im = InventoryManager(loader=dl, sources=[inventory_path])

        # plantuml_output_file = open("generated_plantuml", "w")
        # plantuml_output_file.write('@startuml\n' + Generate.grapher(im) + '@enduml')
        # plantuml_output_file.close()

        result = Generate.graph_group(im.groups["all"])
        formated_result = {"groups": list(dict.fromkeys(result["groups"])), "links": list(dict.fromkeys(result["links"]))}

        click.echo(formated_result)
        # for group_name, group in im.groups.items():
        #     if group.get_name() != "all":
        #         click.echo(group.get_name() + " : " + str(group.get_descendants()))


    @staticmethod
    def graph_group(group, depth=0, result={"groups": [], "links": []}):
        depth += 1
        for kid in group.child_groups:
            click.echo("  "*depth + kid.get_name() + " is descendant of " + group.get_name() + " at depth " + str(depth))
            temp_result = Generate.graph_group(kid, depth, result)
            result["groups"] += temp_result["groups"]
            result["links"] += temp_result["links"]

            if group.get_name() != "all":
                result["links"].append(group.get_name() + "-->" + kid.get_name())
        
        temp_group = ""
        if group.get_name() != "all":
            temp_group = 'rectangle "**' + group.get_name() + '**\n--'.encode("unicode_escape").decode("UTF-8")
            for host in group.hosts:
                temp_group += "\n".encode("unicode_escape").decode("UTF-8") + host.name

            temp_group += '" as rectangle' + str(1) + "\n"
            result["groups"].append(temp_group)
        
        return result


    @staticmethod
    def grapher(im):
        count = 0
        generated_plantuml = ""
        for group, host_list in im.get_groups_dict().items():
            count += 1
            plantuml_group = 'rectangle "**' + group + '**\n--'.encode("unicode_escape").decode("UTF-8")
            for host in host_list:
                plantuml_group += "\n".encode("unicode_escape").decode("UTF-8") + host

            plantuml_group += '" as rectangle' + str(count) + "\n"
            generated_plantuml += plantuml_group

        return generated_plantuml
