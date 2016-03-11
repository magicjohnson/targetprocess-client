# coding=utf-8
"""
TargetProcess API Client
"""
import json
import logging

from urllib import urlencode
from urlparse import parse_qsl, urlparse, urlunparse

import requests

from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, ReadTimeout

from six import add_metaclass

from targetprocess.exceptions import BadResponseError

logger = logging.getLogger(__name__)


class MetaAPI(type):
    RESOURCES = (
        ('story', 'UserStories'),
        ('bug', 'Bugs'),
        ('release', 'Releases'),
    )
    COLLECTIONS = (
        ('stories', 'UserStories'),
        ('bugs', 'Bugs'),
        ('releases', 'Releases'),
        ('iterations', 'TeamIterations'),
    )

    def __init__(cls, name, bases, dct):

        cls._add_resource_methods()
        cls._add_collection_methods()

        super(MetaAPI, cls).__init__(name, bases, dct)

    def _add_resource_methods(cls):
        for resource, tp_name in cls.RESOURCES:
            setattr(cls, "get_{}".format(resource), cls._partial('get_resource', tp_name))
            setattr(cls, "update_{}".format(resource), cls._partial('update_resource', tp_name))

    def _add_collection_methods(cls):
        for collection, tp_name in cls.COLLECTIONS:
            setattr(cls, "get_{}".format(collection), cls._partial('get_collection', tp_name))

    def _partial(cls, method_name, resource_name):
        def func(self, *args, **kwargs):
            return getattr(cls, method_name)(self, resource_name, *args, **kwargs)

        return func


@add_metaclass(MetaAPI)
class TargetProcessAPIClient(object):
    ITEMS_PER_PAGE = 20
    MAX_RETRIES = 1

    def __init__(self, api_url, user, password):
        self.auth = HTTPBasicAuth(user, password)
        self.api_url = api_url
        self.query = {'format': 'json'}

    def get_resource(self, collection, entity_id, paginated=True, **query):
        url = self._build_resource_url(collection, entity_id, **query)
        if paginated:
            return self._get_paginated(url)
        else:
            return self._get(url)

    def get_collection(self, collection, paginated=True, **query):
        if not query.get('take'):
            query.update({'take': self.ITEMS_PER_PAGE})

        url = self._build_resource_url(collection, **query)
        if paginated:
            return self._get_paginated(url)
        else:
            return self._get(url)

    def update_resource(self, collection, entity_id, data):
        url = self._build_resource_url(collection, entity_id, include="[Id]")
        return self._post(url, data)

    def _build_resource_url(self, collection, entity_id=None, **query):
        if entity_id:
            path = '%s/%s' % (collection, entity_id)
        else:
            path = '%s/' % collection

        return self._build_url(path=path, **query)

    def _build_url(self, url=None, path=None, **query_params):
        if not url:
            url = self.api_url

        scheme, host, orig_path, params, orig_query, fragments = urlparse(url)

        query = self._build_query_params(orig_query, **query_params)
        path = "%s/%s" % (orig_path.rstrip('/'), path) if path else orig_path

        return urlunparse((scheme, host, path, params, query, fragments))

    def _build_query_params(self, orig_query, **additional_params):
        """
        Takes original query as a string (i.e `take=100&skip=25`)
        applies default query params from `self.query`
        adds and/or overrides from `**additional_params`
        encodes back to the url string
        """
        query = self.query.copy()
        query.update(dict(parse_qsl(orig_query)))
        query.update(additional_params)
        return urlencode(query)

    def _get(self, url):
        return self._do_request(method='get', url=url)

    def _get_paginated(self, url):
        response = self._get(url)
        if 'Items' in response:
            self._handle_pagination(response)
            for item in response.get('Items', []):
                self._handle_nested_pagination(item)
        else:
            self._handle_nested_pagination(response)
        return response

    def _handle_nested_pagination(self, item):
        nested_items = [(k, v) for k, v in item.iteritems() if isinstance(v, dict)]
        for field, value in nested_items:
            self._handle_pagination(value)

    def _handle_pagination(self, data):
        if 'Next' in data:
            next_page = self._build_url(url=data['Next'])
            next_page_result = self._get(next_page)
            data['Items'] += next_page_result['Items']

    def _post(self, url, data):
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        return self._do_request(method='post', url=url, data=json_data, headers=headers)

    def _do_request(self, method, url, **kwargs):
        attempt = kwargs.pop('attempt', 0)
        try:
            request_method = requests.__getattribute__(method)
            response = request_method(url=url, auth=self.auth, **kwargs)
            if response.status_code != 200:
                raise BadResponseError(response=response)

            return response.json()

        except (ConnectionError, ReadTimeout) as e:
            if attempt < self.MAX_RETRIES:
                attempt += 1
                return self._do_request(url=url, method=method, attempt=attempt, **kwargs)

            logger.exception(e)
            return {}
