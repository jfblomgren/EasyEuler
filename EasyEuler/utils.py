import json
import os
import glob

from jinja2 import Template


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
TEMPLATE_PATH = os.path.join(BASE_PATH, '../templates')


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


def write_to_file(problem, language):
    file_extension = get_file_extension(language)
    file_name = 'euler_%03d%s' % (problem['id'], file_extension)
    template = get_template(language)

    with open(file_name, 'w') as f:
        f.write(template.render(**problem))

    return file_name
