import unittest
import os

from EasyEuler import data
from EasyEuler.cli import cli
from EasyEuler.utils import get_problem

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


class TestGenerateResourcesCommand(CommandTestCase):
    def test_generate_problem_resources(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['generate-resources', '22'])
            self.assertTrue(os.path.exists('names.txt'))

    def test_generate_all_resources(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['generate-resources'])

            for filename in os.listdir('%s/resources' % data.DATA_PATH):
                self.assertTrue(os.path.exists(filename))

    def test_problem_with_no_resources(self):
        result = self.runner.invoke(cli, ['generate-resources', '1'])
        self.assertEqual(result.exit_code, 1)


class TestVerifyCommand(CommandTestCase):
    def test_problem_verification(self):
        with self.runner.isolated_filesystem():
            problem1 = get_problem(1)
            problem2 = get_problem(2)

            with open('euler_001.py', 'w') as f:
                f.write('print(%s)' % problem1['answer'])

            with open('euler_002.py', 'w') as f:
                f.write('print(%s)' % problem2['answer'])

            result = self.runner.invoke(cli, ['verify',
                                              'euler_001.py', 'euler_002.py'])
            output = str(result.output_bytes, encoding='UTF-8')

            self.assertIn(problem1['answer'], output)
            self.assertIn(problem2['answer'], output)

    def test_recursive_verification(self):
        with self.runner.isolated_filesystem():
            os.mkdir('test')
            problem = get_problem(1)

            with open('test/euler_001.py', 'w') as f:
                f.write('print(%s)' % problem['answer'])

            result = self.runner.invoke(cli, ['verify', '--recursive',
                                              'test'])
            output = str(result.output_bytes, encoding='UTF-8')

            self.assertIn(problem['answer'], output)

    def test_show_errors(self):
        with self.runner.isolated_filesystem():
            with open('euler_001.py', 'w') as f:
                f.write('print(')

            result = self.runner.invoke(cli, ['verify', 'euler_001.py'])
            output = str(result.output_bytes, encoding='UTF-8')
            result_with_errors = self.runner.invoke(cli, ['verify', '--errors',
                                        'euler_001.py'])
            output_with_errors = str(result_with_errors.output_bytes,
                                     encoding='UTF-8')

            self.assertIn('[error]', output)
            self.assertIn('SyntaxError', output_with_errors)