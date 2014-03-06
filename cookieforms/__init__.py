"""Main entry point
"""
import os
from pyramid.config import Configurator

APP_DIR = os.path.dirname(os.path.abspath(__file__))


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("cookieforms.views")
    config.add_static_view(
        name='static',
        path=settings.get('cookieforms.static_root',
                          os.path.join(APP_DIR, 'static/')))
    return config.make_wsgi_app()
