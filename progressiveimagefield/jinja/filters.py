from django.template import engines
from django.template.backends.base import BaseEngine
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.files import ImageFieldFile


try:
    from jinja2 import Environment, Markup
except ModuleNotFoundError as e:
    raise ImproperlyConfigured('Jinja2 is not installed!') \
        from ModuleNotFoundError

from progressiveimagefield.templatetags.progressive_tags import \
    render_progressive_field


def progressive(image_field, alt_text=''):
    """
    Used as a Jinja2 filter, this function returns a safe HTML chunk.

    Usage (in the HTML template):

        {{ obj.image|progressive }}

    :param django.db.models.fields.files.ImageFieldFile image_field: image
    :param str alt_text: str
    :return: a safe HTML template ready to be rendered
    """
    if not isinstance(image_field, ImageFieldFile):
        raise ValueError('"image_field" argument must be an ImageField.')

    for engine in engines.all():
        if isinstance(engine, BaseEngine) and hasattr(engine, 'env'):
            env = engine.env
            if isinstance(env, Environment):
                context = render_progressive_field(image_field, alt_text)
                template = env.get_template(
                    'progressiveimagefield/render_field.html'
                )
                rendered = template.render(**context)
                return Markup(rendered)
    return ''
