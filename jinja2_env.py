# from __future__ import absolute_import  # 如果是py2就取消这行的注释
import json
import posixpath

import jinja2
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from urllib.parse import urlparse, urlunparse, urljoin

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters['tojson'] = tojson
    env.filters['url'] = url_filter
    return env


def path_to_url(path):
    """Convert a system path to a URL."""

    return '/'.join(path.split('\\'))


def get_relative_url(url, other):
    """
    Return given url relative to other.
    """
    if other != '.':
        # Remove filename from other url if it has one.
        parts = posixpath.split(other)
        other = parts[0] if '.' in parts[1] else other
    relurl = posixpath.relpath(url, other)
    return relurl + '/' if url.endswith('/') else relurl


def normalize_url(path, page=None, base=''):
    """ Return a URL relative to the given page or using the base. """
    path = path_to_url(path or '.')
    # Allow links to be fully qualified URL's
    parsed = urlparse(path)
    if parsed.scheme or parsed.netloc or path.startswith(('/', '#')):
        return path

    # We must be looking at a local path.
    if page is not None:
        return get_relative_url(path, page.url)
    else:
        return posixpath.join(base, path)


@jinja2.contextfilter
def url_filter(context, value):
    """ A Template filter to normalize URLs. """
    return normalize_url(value, page=context['page'], base=context['base_url'])


def tojson(obj, **kwargs):
    return jinja2.Markup(json.dumps(obj, **kwargs))
