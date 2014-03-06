# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='cookieforms',
      version='0.1.dev0',
      description='cookieforms',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author=u'Rémy HUBSCHER',
      author_email='hubscher.remy@gmail.com',
      url='https://github.com/diecutter/cookieforms',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['cornice', 'waitress', 'requests', 'pyramid_jinja2'],
      entry_points={
          'paste.app_factory': [
              'main = cookieforms:main',
          ]
      })
