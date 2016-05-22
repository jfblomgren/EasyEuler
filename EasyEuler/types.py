import click


from .utils import get_problem


class ProblemType(click.ParamType):
    name = 'integer'

    def convert(self, value, param, ctx):
        try:
            return get_problem(int(value)) if value is not None else None
        except ValueError:
            self.fail('%s is not a valid integer' % value, param, ctx)
        except IndexError:
            self.fail('A problem with ID %s does not exist' % value, param, ctx)
