import click


from .utils import get_problem


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
