# -*- encoding: utf-8 -*-

"""
This module provides a simple python wrapper over the LogMeIn REST API.
"""

from .vendor.requests import Session

from .config import config


#: Default timeout for each request. 180 seconds connect, 180 seconds read.
TIMEOUT = 180


class Client(object):
    def __init__(self, endpoint=None, company_id=None,
                 psk=None, timeout=TIMEOUT, config_file=None):
        """
        Creates a new Client. No credential check is done at this point.
        """
        # Load a custom config file if requested
        if config_file is not None:
            config.read(config_file)

        # load endpoint
        if endpoint is None:
            self._endpoint = config.get('default', 'endpoint')
        else:
            self._endpoint = endpoint

        # load keys
        if company_id is None:
            company_id = config.get(endpoint, 'company_id')
        self._company_id = company_id

        if psk is None:
            psk = config.get(endpoint, 'psk')
        self._psk = psk

        # use a requests session to reuse HTTPS connections between requests
        self._session = Session()

        # Override default timeout
        self._timeout = timeout
