Progressive Image Model Field for Django
----------------------------------------

Requires:

-  Python 3.6+
-  Pillow 4.0+
-  Django 1.10+

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

Finally, inside another template where you want to render your image
progressively:

.. code:: html

    {% load progressive_tags %}

    {% block content %}
        {% render_progressive_field instance.img %}
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
