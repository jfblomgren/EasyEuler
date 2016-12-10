import os
import unittest

from click.testing import CliRunner

from EasyEuler import data, paths
from EasyEuler.cli import cli


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
            result = self.runner.invoke(cli, ['create', '1', 'python'],
                                        input='n\n')

            self.assertTrue(os.path.getsize('euler_001.py') == 0)

    def test_overwrite(self):
        with self.runner.isolated_filesystem():
            open('euler_001.py', 'a').close()
            result = self.runner.invoke(cli, ['create', '1', 'python'],
                                        input='y\n')

            self.assertTrue(os.path.getsize('euler_001.py') > 0)

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

            for filename in os.listdir(paths.RESOURCES):
                self.assertTrue(os.path.exists(filename))

    def test_problem_with_no_resources(self):
        result = self.runner.invoke(cli, ['generate-resources', '1'])
        self.assertEqual(result.exit_code, 1)


class TestVerifyCommand(CommandTestCase):
    def test_problem_verification_with_execution_only(self):
        with self.runner.isolated_filesystem():
            problem1 = data.problems[1]
            problem2 = data.problems[2]

            with open('euler_001.py', 'w') as f:
                f.write('print(%s)' % problem1['answer'])

            with open('euler_002.py', 'w') as f:
                f.write('print(%s)' % problem2['answer'])

            result = self.runner.invoke(cli, ['verify',
                                              'euler_001.py', 'euler_002.py'])
            output = str(result.output_bytes, encoding='UTF-8')

            self.assertIn(problem1['answer'], output)
            self.assertIn(problem2['answer'], output)

    def test_problem_verification_with_build_and_cleanup(self):
        problem = data.problems[1]
        with self.runner.isolated_filesystem():
            with open('euler_001.c', 'w') as f:
                f.writelines(['#include <stdio.h>\n',
                              'int main(void) {\n',
                              'printf("%s");\n' % problem['answer'],
                              'return 0;\n',
                              '}\n'])

            result = self.runner.invoke(cli, ['verify', '-e', 'euler_001.c'])
            output = str(result.output_bytes, encoding='UTF-8')

            self.assertIn(problem['answer'], output)
            self.assertFalse(os.path.exists('euler_001.c.out'))

    def test_recursive_verification(self):
        with self.runner.isolated_filesystem():
            os.mkdir('test')
            problem = data.problems[1]

            with open('test/euler_001.py', 'w') as f:
                f.write('print(%s)' % problem['answer'])

            result = self.runner.invoke(cli, ['verify', '--recursive',
                                              'test'])
            output = str(result.output_bytes, encoding='UTF-8')

            self.assertIn(problem['answer'], output)

    def test_show_execute_errors(self):
        with self.runner.isolated_filesystem():
            with open('euler_001.py', 'w') as f:
                f.write('print(')

            result = self.runner.invoke(cli, ['verify', 'euler_001.py'])
            output = str(result.output_bytes, encoding='UTF-8')
            result_with_errors = self.runner.invoke(cli, ['verify', '--errors',
                                                          'euler_001.py'])
            output_with_errors = str(result_with_errors.output_bytes,
                                     encoding='UTF-8')

            self.assertIn('[error during execute]', output)
            self.assertIn('SyntaxError', output_with_errors)

    def test_show_build_errors(self):
        with self.runner.isolated_filesystem():
            with open('euler_001.c', 'w') as f:
                f.write('#include <invalid_header.h>')

            result = self.runner.invoke(cli, ['verify', 'euler_001.c'])
            output = str(result.output_bytes, encoding='UTF-8')
            result_with_errors = self.runner.invoke(cli, ['verify', '--errors',
                                                          'euler_001.c'])
            output_with_errors = str(result_with_errors.output_bytes,
                                     encoding='UTF-8')

            self.assertIn('[error during build]', output)
            self.assertIn('fatal error: invalid_header.h', output_with_errors)
