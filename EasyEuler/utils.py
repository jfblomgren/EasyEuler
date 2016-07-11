from EasyEuler import data


def get_problem(problem_id):
    return data.problems[problem_id - 1] if len(data.problems) >= problem_id else None


def get_language(name):
    for language in data.config['languages']:
        if language['name'] == name:
            return language
    return None
