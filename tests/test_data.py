import unittest

from EasyEuler.data import ProblemList, ConfigurationDictionary


class TestProblemList(unittest.TestCase):
    def setUp(self):
        problem_list = [1, 2, 3]
        self.problems = ProblemList(problem_list)

    def test_get_item(self):
        problem = self.problems[1]
        self.assertEqual(problem, 1)

    def test_get_valid_id(self):
        problem = self.problems.get(3)
        self.assertIsNotNone(problem)

    def test_get_invalid_id(self):
        problem1 = self.problems.get(0)
        problem2 = self.problems.get(99999)

        self.assertIsNone(problem1)
        self.assertIsNone(problem2)


class TestConfigurationDictionary(unittest.TestCase):
    def setUp(self):
        config_dict = {
            'foo': 'bar',
            'fuz': 'baz',
            'languages': {
                'python': {
                    'extension': 'py',
                    'template': 'python'
                },
                'c': {
                    'extension': 'c',
                    'template': 'c'
                },
                'ruby': {
                    'extension': 'rb',
                    'template': 'ruby'
                }
            }
        }
        overriding_dict = {
            'fuz': 'qux',
            'languages': {
                'c': {
                    'template': 'cpp'
                },
                'c++': {
                    'extension': 'cpp',
                    'template': 'cpp'
                }
            }
        }
        self.config = ConfigurationDictionary([config_dict, overriding_dict])

    def test_update(self):
        self.assertEqual(self.config['fuz'], 'qux')
        self.assertEqual(self.config['languages']['c']['template'], 'cpp')
        self.assertEqual(self.config['languages']['c']['extension'], 'c')
        self.assertEqual(self.config['languages']['c++']['template'], 'cpp')
        self.assertEqual(self.config['languages']['c++']['extension'], 'cpp')

    def test_get_item(self):
        self.assertEqual(self.config['foo'], 'bar')

    def test_get_language(self):
        python = self.config.get_language('extension', 'py')
        ruby = self.config.get_language('template', 'ruby')
        invalid_language = self.config.get_language('template', 'foobar')

        self.assertEqual(python['name'], 'python')
        self.assertEqual(ruby['extension'], 'rb')
        self.assertIsNone(invalid_language)
