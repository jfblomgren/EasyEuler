from EasyEuler import data


def get_problem(problem_id):
    return data.problems[problem_id - 1] if len(data.problems) >= problem_id else None


def get_language(value, key='name'):
    for language in data.config['languages']:
        if language[key] == value:
            return language
    return None
