import json
import subprocess
import os
import glob
import re

from jinja2 import Environment, FileSystemLoader


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
TEMPLATE_PATH = os.path.join(BASE_PATH, '../templates')
CONFIG_PATH = os.path.join(BASE_PATH, '../config.json')

templates = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

with open(CONFIG_PATH) as f:
    config = json.load(f)

with open('%s/problems.json' % DATA_PATH) as f:
    problems = json.load(f)


def get_problem(problem_id):
    return problems[problem_id - 1] if len(problems) >= problem_id else None


def get_language(name):
    for language in config['languages']:
        if language['name'] == name:
            return language
    return None


def write_to_file(problem, language, path=None, overwrite=False):
    template = templates.get_template(language.get('template',
                                                   language['name']))

    if path is None:
        path = 'euler_%03d.%s' % (problem['id'], language['extension'])

    if os.path.exists(path) and not overwrite:
        return (path, False)

    with open(path, 'w') as f:
        f.write(template.render(**problem))

    return (path, True)


def get_problem_id(path):
    problem_id = re.findall(r'\D*([1-9]\d{0,2}).*', path)
    return int(problem_id[0]) if len(problem_id) > 0 else None


def get_language_from_file_extension(file_extension):
    for language in config['languages']:
        if language['extension'] == file_extension:
            return language
    return None


def verify_solution(path, problem_id=None, language=None):
    if language is None:
        file_extension = os.path.splitext(path)[1].replace('.', '')
        language = get_language_from_file_extension(file_extension)

    problem = get_problem(problem_id)
    process = subprocess.run(language['command'].format(path=path), shell=True,
                             stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    output = str(process.stdout, encoding='UTF-8').replace('\n', '')

    if process.returncode > 0:
        status = 'E'
    elif output == problem['answer']:
        status = 'C'
    else:
        status = 'I'

    return status, output
