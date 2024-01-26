import unittest
from click.testing import CliRunner
from ansible_inventory_to_schema.cli import generate


class TestAnsibleInventoryToSchema(unittest.TestCase):
    def test_generate(self):
        runner = CliRunner()
        result = runner.invoke(generate)
        assert result.exit_code == 0
        assert result.output == 'Hello World\n'
