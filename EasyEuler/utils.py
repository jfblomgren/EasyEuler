import json
import subprocess
import os
import glob
import re

from jinja2 import Template


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
TEMPLATE_PATH = os.path.join(BASE_PATH, '../templates')
CONFIG_PATH = os.path.join(BASE_PATH, '../config.json')


def get_problem(problem_id):
    with open('%s/problems.json' % DATA_PATH) as f:
        problems = json.load(f)
    return problems[problem_id - 1] if len(problems) >= problem_id else None


def get_template_path(language):
    matching_files = glob.glob('%s/%s.*' % (TEMPLATE_PATH, language))
    return matching_files[0] if len(matching_files) > 0 else None


def get_template(language):
    template_path = get_template_path(language)

    if template_path is None:
        return None

    with open(template_path) as f:
        return Template(f.read())


def get_file_extension(language):
    template_path = get_template_path(language)
    return os.path.splitext(template_path)[1]


def write_to_file(problem, language, path=None, overwrite=False):
    file_extension = get_file_extension(language)
    template = get_template(language)

    if path is None:
        path = 'euler_%03d%s' % (problem['id'], file_extension)

    if os.path.exists(path) and not overwrite:
        return (path, False)

    with open(path, 'w') as f:
        f.write(template.render(**problem))

    return (path, True)


def get_problem_id(path):
    problem_id = re.findall(r'\D*([1-9]\d{0,2}).*', path)
    return int(problem_id[0]) if len(problem_id) > 0 else None


def get_language_from_file_extension(file_extension):
    matching_files = glob.glob('%s/*%s' % (TEMPLATE_PATH, file_extension))

    if len(matching_files) > 0:
        file_name = os.path.basename(matching_files[0])
        return os.path.splitext(file_name)[0]
    return None


def get_command(language):
    with open(CONFIG_PATH) as f:
        commands = json.load(f)
    return commands.get(language)


def verify_solution(path, problem_id=None, language=None):
    if language is None:
        file_extension = os.path.splitext(path)[1]
        language = get_language_from_file_extension(file_extension)

    problem = get_problem(problem_id)
    command = get_command(language).format(path=path)
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output = str(process.stdout, encoding='UTF-8').replace('\n', '')

    if process.returncode > 0:
        status = 'E'
    elif output == problem['answer']:
        status = 'C'
    else:
        status = 'I'

    return status, output
