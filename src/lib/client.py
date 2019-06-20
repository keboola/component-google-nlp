import logging
import requests
import sys
from kbc.client_base import HttpClientBase

BASE_URL = 'https://language.googleapis.com/v1'

class googleNLPClient(HttpClientBase):

    def __init__(self, token):

        _def_params = {'key': token}
        self.token = token

        HttpClientBase.__init__(base_url=BASE_URL, max_retries=10,
                                backoff_factor=0.3, default_params=_def_params,
                                status_forcelist=(403, 500, 502))

    