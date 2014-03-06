CookieForms
===========

cookieforms is a simple wsgi server that take a cookiecutter template
repository and build a JSONForm.

Then you just submit the form and download the response using diecutter.

Just do:

    GET /:owner/:repo/?[access_token=<your_token>]&[ref=master]

And that's all.


Run the service
+++++++++++++++

    pserve cookieforms.ini


Run with WSGI
+++++++++++++

.. code:: python

    # -*- coding: utf-8 -*-
    import os

    cfg_dir = os.path.dirname(__file__)
    env_dir = os.path.join(cfg_dir, 'var', 'venv')

    activate_this = os.path.join(env_dir, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    from pyramid.paster import get_app, setup_logging
    ini_path = os.path.join(cfg_dir, 'cookieforms.ini')
    setup_logging(ini_path)
    application = get_app(ini_path, 'main')
