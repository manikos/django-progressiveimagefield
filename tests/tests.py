import os
import re
from pathlib import Path
from PIL import Image

from django.core.files import File
from django.test.testcases import TestCase

from jinja2 import Markup

from .test_settings import MEDIA_URL, MEDIA_ROOT
from .models import TestModel
from progressiveimagefield.jinja.filters import progressive
from progressiveimagefield.templatetags.progressive_tags import (
    _calc_aspect_ratio, _get_thumbnail_url, render_progressive_field
)

REL_PATH_FILENAME = 'tests/local_test_images'


def empty_image_dir():
    for image in os.scandir(MEDIA_ROOT):
        os.remove(image)


def create_model_instance(name, img_name):
    image_file = File(
        open(Path(f'{REL_PATH_FILENAME}/{img_name}'), 'rb')
    )
    obj = TestModel(name=name, img=image_file)
    obj.img.save(img_name, image_file)
    obj.save()
    return obj


class ProgressiveImageFieldTestCase(TestCase):

    def setUp(self):
        self.obj = create_model_instance(
            name='aurora',
            img_name='aurora-borealis.jpg'
        )
        self.thumbnail = Image.open(
            f'{MEDIA_ROOT}/aurora-borealis_thumb.jpg'
        )

    def tearDown(self):
        empty_image_dir()

    def test_indexed_image_conversion(self):
        """ Check if an indexed mode image can be converted to RGB """
        png = Image.open(f'{REL_PATH_FILENAME}/500x500.png')
        self.assertEqual(png.mode, 'P')
        png_rgb = png.convert('RGB')
        self.assertEqual(png_rgb.mode, 'RGB')

    def test_thumb_existence(self):
        """ Ensure that thumbnail is created. """
        f = Path(self.thumbnail.filename)
        self.assertTrue(f.exists())

    def test_thumb_format(self):
        """ Ensure thumbnail is a jpeg image """
        self.assertEqual(self.thumbnail.format, 'JPEG')

    def test_thumb_dimensions(self):
        """
        Ensure that dimensions of generated thumbnail is less than
        or equal to 10x10px.
        """
        self.assertLessEqual(self.thumbnail.size, (10, 10))


class TemplateTagsTestCase(TestCase):

    def setUp(self):
        self.portrait = create_model_instance(
            name='portrait',
            img_name='100x500.jpg'
        )
        self.landscape = create_model_instance(
            name='landscape',
            img_name='500x100.JPG'
        )
        self.square = create_model_instance(
            name='square',
            img_name='500x500.png'
        )
        self.decimal = create_model_instance(
            name='decimal',
            img_name='125x133.jpg'
        )

    def tearDown(self):
        empty_image_dir()

    def test_calc_aspect_ratio(self):
        self.assertEqual(_calc_aspect_ratio(self.portrait.img), 500)
        self.assertEqual(_calc_aspect_ratio(self.landscape.img), 20)
        self.assertEqual(_calc_aspect_ratio(self.square.img), 100)
        self.assertEqual(_calc_aspect_ratio(self.decimal.img), 106.4)

    def test_get_thumbnail_url(self):
        self.assertEqual(
            _get_thumbnail_url(self.portrait.img),
            f'{MEDIA_URL}100x500_thumb.jpg'
        )
        self.assertEqual(
            _get_thumbnail_url(self.landscape.img),
            f'{MEDIA_URL}500x100_thumb.JPG'
        )
        self.assertEqual(
            _get_thumbnail_url(self.square.img),
            f'{MEDIA_URL}500x500_thumb.png'
        )

    def test_render_progressive_field_empty_alt(self):
        context = render_progressive_field(self.portrait.img)
        correct_context = {
            'image': self.portrait.img,
            'thumb_url': '/media/100x500_thumb.jpg',
            'alt': '',
            'ar_percent': 500,
        }
        self.assertEqual(context, correct_context)

    def test_render_progressive_field_non_empty_alt(self):
        context = render_progressive_field(self.portrait.img, 'alt_text')
        correct_context = {
            'image': self.portrait.img,
            'thumb_url': '/media/100x500_thumb.jpg',
            'alt': 'alt_text',
            'ar_percent': 500,
        }
        self.assertEqual(context, correct_context)


class Jinja2TestCase(TestCase):
    def setUp(self):
        self.portrait = create_model_instance(
            name='portrait',
            img_name='100x500.jpg'
        )

    def tearDown(self):
        empty_image_dir()

    def test_progressive(self):
        context = render_progressive_field(self.portrait.img, 'alt_text')
        rendered_html_text = progressive(self.portrait.img, context['alt'])
        correct_text = Markup(
            f'<div class="placeholder" data-large="{context["image"].url}">'
            f'<img class="img-small" src="{context["thumb_url"]}" '
            f'alt="{context["alt"]}">'
            f'<div style="padding-bottom:{context["ar_percent"]}%;"></div>'
            f'</div>'
        )
        texts = [re.sub(r'[\n\t]*', '', t)
                 for t in [rendered_html_text, correct_text]]
        self.assertEqual(texts[0], texts[1])
