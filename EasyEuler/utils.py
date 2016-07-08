import time
import subprocess
import os
import re
import resource
import shutil

from EasyEuler import data


PROBLEM_ID_REGEX = re.compile(r'\D*([1-9]\d{0,2}).*')


def get_problem(problem_id):
    return data.problems[problem_id - 1] if len(data.problems) >= problem_id else None


def get_language(name):
    for language in data.config['languages']:
        if language['name'] == name:
            return language
    return None


def write_to_file(problem, language, path=None, overwrite=False):
    template = data.templates.get_template(language.get('template',
                                                        language['name']))

    if path is None:
        path = 'euler_%03d.%s' % (problem['id'], language['extension'])

    if os.path.exists(path) and not overwrite:
        return (path, False)

    with open(path, 'w') as f:
        f.write(template.render(**problem))

    return (path, True)


def get_problem_id(path):
    problem_id = PROBLEM_ID_REGEX.findall(path)
    return int(problem_id[0]) if len(problem_id) > 0 else None


def get_language_from_file_extension(file_extension):
    for language in data.config['languages']:
        if language['extension'] == file_extension:
            return language
    return None


def verify_solution(path, time_execution, problem_id=None, language=None):
    if language is None:
        file_extension = os.path.splitext(path)[1].replace('.', '')
        language = get_language_from_file_extension(file_extension)

    problem = get_problem(problem_id)
    command = './{path}' if language is None else language['command']
    process, execution_time = execute_process(command.format(path=path),
                                              time_execution)

    if process.returncode != 0:
        status = 'E'
        output = str(process.stderr, encoding='UTF-8')
    else:
        output = str(process.stdout, encoding='UTF-8').replace('\n', '')
        if output == problem['answer']:
            status = 'C'
        else:
            status = 'I'

    return status, output, execution_time


def execute_process(command, time_execution):
    if time_execution:
        start_time = get_time()
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        end_time = get_time()

        execution_time = {key: end_time[key] - start_time[key]
                          for key in end_time}
    else:
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        execution_time = None

    return process, execution_time


def get_time():
    rs = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {'user': rs.ru_utime, 'system': rs.ru_stime,
            'total': rs.ru_stime + rs.ru_utime, 'wall': time.time()}


def generate_problem_resources(problem, path):
    for file_name in problem['resources']:
        shutil.copy('%s/resources/%s' % (data.DATA_PATH, file_name), path)


def generate_all_resources(path):
    for problem in data.problems:
        if 'resources' in problem:
            generate_problem_resources(problem, path)
