import unittest
import os

from EasyEuler.cli import commands

from click.testing import CliRunner


class CommandLineInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()


class TestGenerateCommand(CommandLineInterfaceTestCase):
    def test_file_creation(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(commands, ['generate', '1'])
            self.runner.invoke(commands, ['generate', '1', 'c'])

            self.assertTrue(os.path.exists('euler_001.py'))
            self.assertTrue(os.path.exists('euler_001.c'))

    def test_invalid_problem_id(self):
        result = self.runner.invoke(commands, ['generate', '9999'])
        self.assertEqual(result.exit_code, 1)


if __name__ == '__main__':
    unittest.main()
