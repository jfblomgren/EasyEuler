from EasyEuler import data


def get_problem(problem_id):
    if problem_id < 1 or len(data.problems) < problem_id:
        # We don't want a negative index, because it'll wrap back around.
        return None
    return data.problems[problem_id - 1]


def get_language(value, key='name'):
    for language in data.config['languages']:
        if language[key] == value:
            return language
    return None
