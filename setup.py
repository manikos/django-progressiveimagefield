from distutils.core import setup
from setuptools import find_packages

from progressiveimagefield.__init__ import __version__

setup(
    name='django-progressiveimagefield',
    version=__version__,
    description="A Django ImageField that offers progressive \
                image loading during HTML rendering.",
    packages=find_packages(exclude=['tests']),
    long_description=open('README.rst').read(),  # optional
    url='https://github.com/manikos/django-progressiveimagefield',  # optional
    author='Nick Mavrakis',  # optional
    author_email='mavrakis.n@gmail.com',  # optional
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],  # optional
    python_requires='>=3.6',  # optional
    keywords='django progressive image field',  # optional, space separated keywords
    install_requires=['Django>=1.10', 'Pillow>=4.0.0'],  # optional
    zip_safe=False,
    include_package_data=True,
)

