from os.path import splitext

from PIL import Image

from django import template
from django.core.files.images import get_image_dimensions

from progressiveimagefield.fields import THUMB_EXT

register = template.Library()


def _calc_aspect_ratio(image):
    width, height = get_image_dimensions(image)
    aspect_ratio = height / width
    ar_percent = aspect_ratio * 100
    if ar_percent.is_integer():
        ar_percent = int(ar_percent)
    else:
        ar_percent = round(ar_percent, 2)
    return ar_percent

def _get_thumbnail_url(image):
    """ Given a large image, return the thumbnail url """
    lhs, rhs = splitext(image.url)
    lhs += THUMB_EXT
    thumb_url = f'{lhs}{rhs}'
    return thumb_url

@register.inclusion_tag('render_field.html')
def render_progressive_field(image):
    # `image` is an instance of ProgressiveImageField (which is an ImageField)
    ar_percent = _calc_aspect_ratio(image)
    thumb_url = _get_thumbnail_url(image)
    return {
        'image': image,
        'thumb_url': thumb_url,
        'ar_percent': ar_percent,
    }
