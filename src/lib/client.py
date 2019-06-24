from bs4 import BeautifulSoup
import json
import logging
# import os
import requests
import sys
from kbc.client_base import HttpClientBase

BASE_URL = 'https://language.googleapis.com/v1/documents:annotateText'


class googleNLPClient(HttpClientBase):

    def __init__(self, token):

        _def_params = {'key': token}
        _def_header = {"Content-Type": "application/json",
                       "Accept": "application/json"}
        self.token = token

        HttpClientBase.__init__(self, base_url=BASE_URL, max_retries=10,
                                backoff_factor=0.3, default_params=_def_params,
                                status_forcelist=(403, 500, 502), default_http_header=_def_header)

        self._check_token()

    def _check_token(self):

        _body = self._create_body('', '', {})

        # Will produce a 400 error due to invalid payload.
        # Depending on message, the token can be verified
        _rsp = self.post_raw(self.base_url, data=_body)
        _sc = _rsp.status_code
        _msg = _rsp.json()['error'].get('message')

        if 'API key not valid' in _msg:

            logging.error("Please check the API token.")
            logging.error(
                "The API token could not be verified. The response received was %s: %s" % (_sc, _msg))

            sys.exit(1)

        else:

            logging.info("Verified API token.")

    def _get_supported_languages(self):

        # No API call to obtain supported languages in Google NLP.
        # Will perform a scrape once in a while to ensure languages are supported.

        _map = {'content_classification': 'classifyText',
                'syntactic_analysis': 'analyzeSyntax',
                'entity_analysis': 'analyzeEntities',
                'sentiment_analysis': 'analyzeSentiment',
                'entity_sentiment_analysis': 'analyzeEntitySentiment'}

        _page = self.get_raw('https://cloud.google.com/natural-language/docs/languages')
        soup = BeautifulSoup(_page.text, "html.parser")

        table_headers = soup.findAll('h2')
        table_contents = soup.findAll('table')

        if len(table_contents) != len(table_headers):

            logging.info("Skipping obtaining languages due to not matching website inputs.")
            return

        supported_languages = {}
        try:
            for t in range(len(table_headers)):

                _name = table_headers[t]['id']
                _name_mapped = _map.get(_name)

                _table = table_contents[t].select('tbody > tr > td > code')

                supported_languages[_name_mapped] = [l.text for l in _table]

            return supported_languages

        except (KeyError, AttributeError) as e:

            logging.warn("Could not obtain languages.")
            logging.warn(e)

    def _create_body(self, content, language, features, inputType='PLAIN_TEXT'):

        if language is None:

            language = ''

        _template = {"document": {"type": inputType,
                                  "content": content,
                                  "language": language},
                     "encodingType": "UTF8",
                     "features": features}

        logging.debug("Body template:")
        logging.debug(_template)

        return json.dumps(_template)

    def analyze_text(self, content, language, features, inputType='PLAIN_TEXT'):

        _body = self._create_body(content, language, features, inputType)

        try:

            _rsp = self.post_raw(url=self.base_url, data=_body)

            return _rsp

        except requests.exceptions.RetryError as e:

            logging.error(
                "There was a problem calling documents:annotateText endpoint. Retry 10x failed. Reason:")
            logging.error(e)
            logging.debug("Following features were used:")
            logging.debug(str(features))
            logging.error(
                "The issue might be caused by daily limits reached. Please, raise the limits if necessary.")

            sys.exit(2)
