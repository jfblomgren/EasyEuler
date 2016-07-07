import unittest
import os

from EasyEuler.cli import cli

from click.testing import CliRunner


class CommandLineInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()


class TestcreateCommand(CommandLineInterfaceTestCase):
    def test_file_creation(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['create', '1'])
            self.runner.invoke(cli, ['create', '1', 'c'])

            self.assertTrue(os.path.exists('euler_001.py'))
            self.assertTrue(os.path.exists('euler_001.c'))

    def test_invalid_problem_id(self):
        result = self.runner.invoke(cli, ['create', '9999'])
        self.assertEqual(result.exit_code, 2)


if __name__ == '__main__':
    unittest.main()
