Progressive Image Model Field for Django
----------------------------------------

Requires:

-  Python 3.6+
-  Pillow 4.0+
-  Django 2.0+

*The Problem*: So, you have build a website (portfolio, news, eshop
etc), you have optimized your static files (css, js, fonts, images) but
still, the webpage loads quite slow due to lots of images being rendered
(however, there might be other reasons, but right now, let’s focus on
the image rendering).

*The Solution*: Based on `José Manuel
Pérez <https://jmperezperez.com/about-me>`__\ ’s article about `How
Medium does progressive image
loading <https://jmperezperez.com/medium-image-progressive-loading-placeholder>`__,
I have created a Django ModelField, which I called
``ProgressiveImageField``. All it does is this: when an instance’s
progressiveimagefield is created (saved, most commonly via the admin
interface), it automatically creates a very small blurred thumbnail
(maximum dimensions ``10x10px``) next to the original image. When this
large image is rendered, the ``src`` attribute of the ``img`` element
points to the thumbnail and not the large image. So, the user,
initially, sees the blurred thumbnail. Behind the scenes, javascript
takes place and gradually downloads the original image. Once the
original image is downloaded, the blurred thumbnail is replaced through
a nice-looking-CSS-fade effect. That’s all!


Installation
------------

1. Install it using pip:

   ``pip install django-progressiveimagefield``

2. Add it to your ``INSTALLED_APPS`` inside your ``settings`` file:

   ``INSTALLED_APPS += ['progressiveimagefield']``


How to use
----------

Inside your ``models.py``, simply:

.. code:: python

    from django.db import models

    from progressiveimagefield.fields import ProgressiveImageField

    class MyModel(models.Model):
        # Other fields here
        img = ProgressiveImageField(upload_to="somewhere")

Inside your ``base.html`` template:

.. code:: html

    {% load static %}

    <!DOCTYPE html>
    <html>
        <head>
            <!-- other meta tags here etc -->
            <link rel="stylesheet" media="all" href="{% static 'progressiveimagefield/css/pif.css' %}">
        </head>
        <body>
            {% block content %}{% endblock %}
            <script src="{% static 'progressiveimagefield/js/pif.js' %}"></script>
        </body>
    </html>

Finally, inside another HTML template where you want to render your image
progressively, you have two options depending on which template engine is used to render your template:

- Using the DTL (Django Template Language)

    .. code:: html

        {% load progressive_tags %}

        {% block content %}
            {% render_progressive_field instance.img %}
        {% endblock %}

- Using the `Jinja2 Template Language <http://jinja.pocoo.org/>`__

 1. Add the filter inside the file (i.e ``jinja.py``) where Jinja2 Environment is defined

    .. code:: python

        from jinja2 import Environment

        def environment(**options):
            env = Environment(**options)
            env.filters.update({
                'progressive': 'progressiveimagefield.jinja.progressive',
            })
            return env

 2. Add the dotted path to the above function in your ``settings``'s ``TEMPLATES`` setting ``OPTIONS`` dict as the value to the ``environment`` key. OK, here is the code:

    .. code:: python

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.jinja2.Jinja2',
                'DIRS': # setting for DIRS here,
                'APP_DIRS': True,
                'OPTIONS': {
                    'environment': 'path.to.jinja.environment.function',
                },
            },
            ...
        ]

 3. Use it in your HTML template like this (just like a regular Django filter):

    .. code:: html

        {% block content %}
            {{ instance.img|progressive }}
        {% endblock %}


Testing
-------

In order to test this application, you should

1. Clone the repo
2. Create a virtualenv
   (``mkvirtualenv -p $(which python3.6) progressiveimagefield``) and
   activate it (once created, it’ll be activated by default)
3. Install the requirements
   (``pip install -r tests/test_requirements.txt``)
4. Run ``python runtests.py``

Further Reading
---------------

`Page Load Optimization by Progressive Image Loading (like
Medium) <https://blog.botreetechnologies.com/page-load-optimization-by-progressive-image-loading-like-medium-1d0f94744a4d>`__
