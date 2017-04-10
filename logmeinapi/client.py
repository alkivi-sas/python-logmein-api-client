# -*- encoding: utf-8 -*-

"""
This module provides a simple python wrapper over the LogMeIn REST API.
"""

import logging
import requests
import json

from requests.exceptions import RequestException

from .config import config
from .exceptions import APIError


#: Default timeout for each request. 180 seconds connect, 180 seconds read.
TIMEOUT = 180


class Client(object):
    def __init__(self, endpoint=None, company_id=None,
                 psk=None, timeout=TIMEOUT, config_file=None,
                 logger=None):
        """
        Creates a new Client. No credential check is done at this point.
        """
        # Load a custom config file if requested
        if config_file is not None:
            config.read(config_file)

        # load endpoint
        if endpoint is None:
            endpoint = config.get('default', 'endpoint')

        # load keys
        if company_id is None:
            company_id = config.get(endpoint, 'company_id')
        self._company_id = company_id
        if psk is None:
            psk = config.get(endpoint, 'psk')
        self._psk = psk

        # variables we use
        self._authorization = None
        self._root_url = 'https://secure.logmein.com/public-api'

        # init logger
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

        self._session = requests.Session()
        self._session.headers.update({
            'Accept': 'application/JSON; charset=utf-8',
            'Authorization': self.get_authorization(),
        })

        # Override default timeout
        self._timeout = timeout

    def get_authorization(self):
        """Return a json dumps of our authorization."""
        if not self._authorization:
            self._authorization = {'companyId': int(self._company_id),
                                   'psk': self._psk}
        return json.dumps(self._authorization)

    def call(self, method, path, data=None):
        """
        Low level call helper.
        """
        # attempt request
        try:
            result = self.raw_call(method=method, path=path, data=data)
        except RequestException as error:
            raise APIError("Low HTTP request failed error", error)

        status = result.status_code

        # attempt to decode and return the response
        try:
            json_result = result.json()
        except ValueError as error:
            raise APIError("Failed to decode API response", error)

        # error check
        if status >= 100 and status < 300:
            return json_result
        else:
            raise APIError(json_result.get('message'), response=result)

    def raw_call(self, method, path, data=None):
        """
        Lowest level call helper.
        """
        body = ''
        target = self._root_url + path
        headers = {}

        self.logger.debug('Going to {0} on url {1}'.format(method, target))

        # include payload
        if data is not None:
            headers['Content-type'] = 'application/JSON; charset=utf-8'
            body = json.dumps(data)

        return self._session.request(method, target, headers=headers,
                                     data=body, timeout=self._timeout)

    def get(self, _target, **kwargs):
        """
        'GET' :py:func:`Client.call` wrapper.
        """
        return self.call('GET', _target, kwargs)

    def put(self, _target, **kwargs):
        """
        'PUT' :py:func:`Client.call` wrapper.
        """
        return self.put('GET', _target, kwargs)

    def post(self, _target, **kwargs):
        """
        'POST' :py:func:`Client.call` wrapper.
        """
        return self.post('GET', _target, kwargs)

    def delete(self, _target, **kwargs):
        """
        'DELETE' :py:func:`Client.call` wrapper.
        """
        return self.delete('GET', _target, kwargs)

    def test(self):
        path = '/v1/authentication'
        return self.get(path)
