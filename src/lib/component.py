import csv
from hashlib import md5
import json
import logging
import sys
from lib.client import googleNLPClient, GoogleNLPClientException
from lib.result import resultWriter
from kbc.env_handler import KBCEnvHandler


API_KEY = '#API_key'
ANALYSIS_TYPE_KEY = 'analysis_type'
INPUT_TYPE_KEY = 'input_type'

SUPPORTED_ANALYSIS = ['extractEntities', 'extractEntitySentiment', 'classifyText',
                      'extractDocumentSentiment', 'extractSyntax']

SUPPORTED_INPUT = ['PLAIN_TEXT', 'HTML']
MANDATORY_PARS = [API_KEY, ANALYSIS_TYPE_KEY, INPUT_TYPE_KEY]


class Component(KBCEnvHandler):

    def __init__(self):

        KBCEnvHandler.__init__(self, MANDATORY_PARS)
        self.validate_config(MANDATORY_PARS)

        # Parameter fetching
        self.paramToken = self.cfg_params[API_KEY]
        self.paramAnalysisType = self.cfg_params[ANALYSIS_TYPE_KEY]
        self.paramInputType = self.cfg_params[INPUT_TYPE_KEY]

        # Check inputs and create necessary variables for making requests
        self._check_input_tables()
        self._check_parameter_values()
        self._create_request_features()
        self._identify_sentiment()

        self.client = googleNLPClient(token=self.paramToken)
        self.writer = resultWriter(
            methodList=self.paramAnalysisType, dataPath=self.tables_out_path)

    def _create_request_features(self):

        _template = {}

        for _analysis in self.paramAnalysisType:

            _template[_analysis] = True

        self.requestFeatures = _template

    def _identify_sentiment(self):

        _mappingSentiment = {'extractDocumentSentiment': ['documents', 'sentences'],
                             'extractEntitySentiment': ['entities', 'mentions']}

        _includedSentiment = []

        for key in _mappingSentiment:

            if key in self.paramAnalysisType:

                _includedSentiment += _mappingSentiment[key]

            else:

                pass

        logging.debug("Sentiment is present in the following tables:")
        logging.debug(_includedSentiment)

        self.resultSentimentTables = _includedSentiment

    def _check_input_tables(self):

        _input_tables = self.configuration.get_input_tables()

        logging.debug("Input tables:")
        logging.debug(_input_tables)

        if len(_input_tables) == 0:

            logging.error("No input table was provided. Please provide an input table, with mandatory columns \"id\"," +
                          " \"text\" and optional column \"sourceLanguage\". See documentation for more information.")

            sys.exit(1)

        else:

            _input = _input_tables[0]
            _path = _input['full_path']
            _mnfst_path = _path + '.manifest'

            with open(_mnfst_path) as _mnfst_file:

                _mnfst = json.load(_mnfst_file)

                _columns = _mnfst['columns']

                if 'id' in _columns and 'text' in _columns:

                    pass

                else:

                    logging.error(
                        "Missing required column \"id\" or \"text\" in table %s." % _input['destination'])
                    logging.error(
                        "Please, make sure all of the required columns are inputted.")

                    sys.exit(1)

        self.input_table = _input

    def _check_parameter_values(self):

        _setAnalysis = list(set(self.paramAnalysisType) -
                            set(SUPPORTED_ANALYSIS))

        if len(_setAnalysis) != 0:

            logging.error("Unsupported analysis type: %s. Supported types are %s." % (
                _setAnalysis, SUPPORTED_ANALYSIS))

            sys.exit(1)

        if self.paramInputType not in SUPPORTED_INPUT:

            logging.error("Unsupported input type %s. Input type must be one of %s." % (
                self.paramInputType, SUPPORTED_INPUT))

            sys.exit(1)

    def process_document(self, documentDict, retry):

        documentId = documentDict['id']
        documentText = documentDict['text']
        documentLanguage = documentDict.get('sourceLanguage')
        skipCategories = False

        if documentText.strip() == '':

            _message = "The document %s is empty and was skipped." % documentId

            logging.warn(_message)

            self.writer.writerErrors.writerow({'documentId': documentId,
                                               'category': 'emptyDocumentError',
                                               'severity': 'WARNING',
                                               'message': _message})

            return

        _features = self.requestFeatures
        if retry is False:

            _features['classifyText'] = False
            skipCategories = True

        _nlpResponse = self.client.analyze_text(content=documentText, features=_features,
                                                language=documentLanguage, inputType=self.paramInputType)

        _sc = _nlpResponse.status_code
        _js = _nlpResponse.json()

        if _sc == 200:

            self.split_and_write_data(documentId, _js, skipCategories)
            # write results

        elif _sc == 400:

            _message = _js['error']['message']

            if (retry is True and 'Invalid text content: too few tokens' in _message
                    and 'classifyText' in self.paramAnalysisType):

                logging.warn(
                    "Could not use method classifyText for document %s." % documentId)

                if len(self.paramAnalysisType) > 1:

                    _additionalMessage = 'Retrying without classifyText method.'
                    _message = ' '.join([_message, _additionalMessage])

                    self.writer.writerErrors.writerow({'documentId': documentId,
                                                       'category': 'categoryError',
                                                       'severity': 'WARNING',
                                                       'message': _message})

                    logging.info(
                        "Retrying request for document %s without classifyText method." % documentId)

                    self.process_document(documentDict, retry=False)

                    return

                elif len(self.paramAnalysisType) == 1:

                    '''

                    self.writer.writerDocuments.writerow({'documentId': documentId,
                                                          'language': documentLanguage,
                                                          'sentimentMagnitude': '',
                                                          'sentimentScore': ''})

                    '''

                    _additionalMessage = 'Request could not be retried because no other method was specified.'
                    _message = ' '.join([_message, _additionalMessage])

                    logging.warn(_additionalMessage)

                    self.writer.writerErrors.writerow({'documentId': documentId,
                                                       'category': 'categoryError',
                                                       'severity': 'ERROR',
                                                       'message': _message})

                    return

            else:

                _additionalMessage = "Document %s could not be processed. Received:" % documentId
                _logMessage = ' '.join([_additionalMessage, _message])

                logging.warn(_logMessage)

                self.writer.writerErrors.writerow({'documentId': documentId,
                                                   'category': 'nlpError',
                                                   'severity': 'ERROR',
                                                   'message': _message})

                return

    @staticmethod
    def _hash_string(hashList, delim='|'):

        _toHash = '|'.join([str(i) for i in hashList])

        return md5(_toHash.encode()).hexdigest()

    def write_documents(self, documentId, nlpResult):

        if 'documents' in self.resultSentimentTables:

            docSentiment = nlpResult['documentSentiment']['score']
            docMagnitude = nlpResult['documentSentiment']['magnitude']

        else:

            docSentiment, docMagnitude = '', ''

        language = nlpResult['language']

        _writeRowDocuments = {'documentId': documentId,
                              'language': language,
                              'sentimentScore': docSentiment,
                              'sentimentMagnitude': docMagnitude}

        self.writer.writerDocuments.writerow(_writeRowDocuments)

    def write_sentences(self, documentId, nlpResult):

        nlpSentences = nlpResult['sentences']

        idx = -1

        for sentence in nlpSentences:

            idx += 1
            textContent = sentence['text']['content']
            textOffset = sentence['text']['beginOffset']

            if 'sentences' in self.resultSentimentTables:

                senSentiment = sentence['sentiment']['score']
                senMagnitude = sentence['sentiment']['magnitude']

            else:

                senSentiment, senMagnitude = '', ''

            sentenceId = self._hash_string([documentId,
                                            textContent,
                                            textOffset])

            _writerRowSentences = {'sentenceId': sentenceId,
                                   'documentId': documentId,
                                   'index': idx,
                                   'textContent': textContent,
                                   'textOffset': textOffset,
                                   'sentimentScore': senSentiment,
                                   'sentimentMagnitude': senMagnitude}

            self.writer.writerSentences.writerow(_writerRowSentences)

    def write_categories(self, documentId, nlpResult):

        nlpCategories = nlpResult['categories']

        if len(nlpCategories) != 0:

            for category in nlpCategories:

                categoryName = category['name']
                confidence = category['confidence']

                categoryDocumentId = self._hash_string([documentId,
                                                        categoryName])

                _writerRowCategories = {'categoryDocumentId': categoryDocumentId,
                                        'documentId': documentId,
                                        'categoryName': categoryName,
                                        'confidence': confidence}

                self.writer.writerCategories.writerow(_writerRowCategories)

        else:

            _message = "No category detected for document %s." % documentId

            logging.warn(_message)

            self.writer.writerErrors.writerow({'documentId': documentId,
                                               'category': 'categoryError',
                                               'severity': 'WARNING',
                                               'message': _message})

    def write_entities(self, documentId, nlpResult):

        nlpEntities = nlpResult['entities']

        for entity in nlpEntities:

            if 'entities' in self.resultSentimentTables:

                entSentiment = entity['sentiment']['score']
                entMagnitude = entity['sentiment']['magnitude']

            else:

                entSentiment, entMagnitude = '', ''

            name = entity['name']
            entType = entity['type']
            salience = entity['salience']
            metadata = json.dumps(
                entity['metadata']) if entity['metadata'] != {} else ''

            entityId = self._hash_string([documentId, name])

            _writerRowEntities = {'entityId': entityId,
                                  'documentId': documentId,
                                  'name': name,
                                  'type': entType,
                                  'salience': salience,
                                  'metadata': metadata,
                                  'sentimentScore': entSentiment,
                                  'sentimentMagnitude': entMagnitude}

            self.writer.writerEntities.writerow(_writerRowEntities)
            self.write_mentions(entityId, entity)

    def write_mentions(self, entityId, nlpEntity):

        nlpMentions = nlpEntity['mentions']

        for mention in nlpMentions:

            if 'mentions' in self.resultSentimentTables:

                mentSentiment = mention['sentiment']['score']
                mentMagnitude = mention['sentiment']['magnitude']

            else:

                mentSentiment, mentMagnitude = '', ''

            textContent = mention['text']['content']
            textOffset = mention['text']['beginOffset']
            mentType = mention['type']

            mentionId = self._hash_string([entityId, textContent, textOffset])

            _writerRowMentions = {'mentionId': mentionId,
                                  'entityId': entityId,
                                  'textContent': textContent,
                                  'textOffset': textOffset,
                                  'type': mentType,
                                  'sentimentScore': mentSentiment,
                                  'sentimentMagnitude': mentMagnitude}

            self.writer.writerMentions.writerow(_writerRowMentions)

    @staticmethod
    def flatten_json(js, out={}, name='', delim='_'):
        if type(js) is dict:
            for a in js:
                Component.flatten_json(js[a], out, name + a + delim)
        else:
            out[name[:-1]] = js

        return out

    def write_tokens(self, documentId, nlpResult):

        nlpTokens = nlpResult['tokens']

        idx = -1

        for token in nlpTokens:

            idx += 1

            textContent = token['text']['content']
            textOffset = token['text']['beginOffset']

            _flatToken = self.flatten_json(js=token)

            tokenId = self._hash_string([documentId,
                                         textContent,
                                         textOffset,
                                         idx])

            _writerRowTokens = {**{'tokenId': tokenId,
                                   'documentId': documentId,
                                   'textContent': textContent,
                                   'textOffset': textOffset,
                                   'index': idx},
                                **_flatToken}

            self.writer.writerTokens.writerow(_writerRowTokens)

    def split_and_write_data(self, documentId, nlpResult, skipCategories=False):

        for table in self.writer.resultTableNames:

            # Mentions are automatically created with entities and are its child
            # Errors are logged separately
            if table in ['mentions', 'errors']:

                continue

            elif skipCategories is True:

                continue

            else:

                f = eval('self.write_' + table)
                f(documentId, nlpResult)

    def run(self):

        _path = self.input_table['full_path']

        with open(_path) as fileInput:

            _reader = csv.DictReader(fileInput)

            for row in _reader:

                try:
                    self.process_document(documentDict=row, retry=True)
                except GoogleNLPClientException as e:
                    raise e

                if _reader.line_num % 250 == 0:

                    logging.info("Made %s call to API so far." % _reader.line_num)
