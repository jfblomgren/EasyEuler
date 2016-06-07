import click


from .utils import get_problem, get_language


class ProblemType(click.ParamType):
    name = 'integer'

    def convert(self, value, param, ctx):
        if value is None:
            return None

        try:
            problem = get_problem(int(value))
        except ValueError:
            self.fail('%s is not a valid integer' % value, param, ctx)

        if problem is None:
            self.fail('A problem with ID %s does not exist' % value, param, ctx)

        return problem


class LanguageType(click.ParamType):
    name = 'string'

    def convert(self, value, param, ctx):
        if value is None:
            return None

        language = get_language(value)

        if language is None:
            self.fail('Could not find language %s' % value, param, ctx)

        return language
