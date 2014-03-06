""" Cornice services.
"""
import json
import logging
import pkg_resources
import requests

from cornice import Service
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.renderers import render_to_response

from cookieforms.utils import build_json_form

logger = logging.getLogger(__package__)

hello = Service(name='hello', path='/', description='Hello page')


@hello.get()
def get_hello(request):
    return render_to_response(
        'index.jinja2',
        {'hello': 'Go to /{owner}/{repo}/',
         'params': {'access_token': 'OAuth token',
                    'ref': 'branch, tag or commit reference'},
         'source': 'https://github.com/diecutter/cookieforms',
         'version': pkg_resources.get_distribution(__package__).version},
        request=request)


rawfile = Service(name='cookieforms',
                  path='/{owner}/{repo}/',
                  description="Load a CookieCutter Template")


@rawfile.get()
def get_info(request):
    """Returns the file content from github."""
    owner = request.matchdict['owner']
    repo = request.matchdict['repo']
    file_path = 'cookiecutter.json'

    url = 'https://api.github.com/repos/{owner}/{repo}/' \
          'contents/{file_path}?'.format(
              owner=owner,
              repo=repo,
              file_path=file_path)

    access_token = request.params.get('access_token')
    ref = request.params.get('ref')

    if ref:
        url += 'ref={ref}&'.format(ref=ref)

    logger.debug('URL: %s' % url)

    if access_token:
        url += 'access_token={access_token}'.format(access_token=access_token)

    r = requests.get(url,
                     headers={'Accept': 'application/vnd.github.V3.raw'})
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.debug('URL: %s' % url)
        logger.debug(str(e))
        return HTTPFound(
            'https://github.com/{owner}/{repo}/raw/{ref}/{file_path}'.format(
                owner=owner, repo=repo,
                ref=ref or 'master', file_path=file_path))

    try:
        cookiecutter_conf = json.loads(r.text)
    except ValueError:
        return HTTPBadRequest(
            'https://github.com/{owner}/{repo}/raw/{ref}/{file_path}'.format(
                owner=owner, repo=repo, ref=ref or 'master',
                file_path=file_path) + ' is not a JSON file.')

    json_form = build_json_form(cookiecutter_conf)

    return render_to_response('form.jinja2',
                              {'form_schema': json.dumps(json_form['schema']),
                               'owner': owner,
                               'repo': repo},
                              request=request)
