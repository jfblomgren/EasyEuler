import unittest
import os

from EasyEuler.cli import cli

from click.testing import CliRunner


class CommandTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()


class TestCreateCommand(CommandTestCase):
    def test_file_creation(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['create', '1'])
            self.runner.invoke(cli, ['create', '1', 'c'])

            self.assertTrue(os.path.exists('euler_001.py'))
            self.assertTrue(os.path.exists('euler_001.c'))

    def test_file_already_exists(self):
        with self.runner.isolated_filesystem():
            open('euler_001.py', 'a').close()
            result = self.runner.invoke(cli, ['create', '1', 'python'])

            self.assertEqual(result.exit_code, 1)

    def test_overwrite(self):
        with self.runner.isolated_filesystem():
            open('euler_001.py', 'a').close()
            result = self.runner.invoke(cli, ['create', '--overwrite',
                                              '1', 'python'])

            self.assertTrue(os.path.getsize('euler_001.py') > 0)
            self.assertEqual(result.exit_code, 0)

    def test_path(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['create', '--path', 'test.py',
                                     '1', 'python'])

            self.assertTrue(os.path.exists('test.py'))

    def test_invalid_problem_id(self):
        result = self.runner.invoke(cli, ['create', '0'])
        self.assertEqual(result.exit_code, 2)


if __name__ == '__main__':
    unittest.main()
