from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.filters.update({
        'progressive': 'progressiveimagefield.jinja.progressive',
    })
    return env
