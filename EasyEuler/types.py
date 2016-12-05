import click

from EasyEuler import data


class ProblemType(click.ParamType):
    name = 'integer'

    def convert(self, value, param, ctx):
        if value is None:
            return None

        try:
            problem = data.problems.get(int(value))
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

        language = data.config['languages'].get(value)

        if language is None:
            self.fail('Could not find language %s' % value, param, ctx)

        return {'name': value, **language}
