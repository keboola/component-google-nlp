import csv
import json
import logging
import os
from kbc.result import KBCResult, KBCTableDef

# First column used as ID
FIELDS_ENTITIES = ['entityId', 'documentId', 'name', 'type',
                   'salience', 'metadata', 'sentimentMagnitude',
                   'sentimentScore']

FIELDS_MENTIONS = ['mentionId', 'entityId', 'textContent', 'textOffset',
                   'type', 'sentimentMagnitude', 'sentimentScore']

FIELDS_DOCUMENTS = ['documentId', 'language', 'sentimentMagnitude', 'sentimentScore']

FIELDS_SENTENCES = ['sentenceId', 'documentId', 'index', 'textContent', 'textOffset',
                    'sentimentMagnitude', 'sentimentScore']

FIELDS_CATEGORIES = ['categoryDocumentId', 'documentId', 'categoryName', 'confidence']

FIELDS_TOKENS = ['tokenId', 'documentId', 'textContent', 'textOffset', 'lemma', 'index',
                 'partOfSpeech_tag', 'partOfSpeech_aspect', 'partOfSpeech_case',
                 'partOfSpeech_form', 'partOfSpeech_gender', 'partOfSpeech_mood',
                 'partOfSpeech_number', 'partOfSpeech_person', 'partOfSpeech_proper',
                 'partOfSpeech_reciprocity', 'partOfSpeech_tense', 'partOfSpeech_voice',
                 'dependencyEdge_headTokenIndex', 'dependencyEdge_label']

FIELDS_ERRORS = ['documentId', 'category', 'severity', 'message']


class resultWriter:

    def __init__(self, methodList, dataPath):

        self.paramMethods = methodList
        self.paramDataPath = dataPath

        self.create_writers()
        self.create_manifests()

    def _create_table_definition(self, tableName, tableColumns):

        _pk = tableColumns[0]
        _fileName = tableName + '.csv'
        _full_path = os.path.join(self.paramDataPath, _fileName)

        _tbl_def = KBCTableDef(name=tableName, columns=tableColumns, pk=[_pk])
        _result_def = KBCResult(file_name=_fileName, full_path=_full_path, table_def=_tbl_def)

        return _result_def

    @staticmethod
    def _create_csv_writer(tableDefinition):

        _writer = csv.DictWriter(open(tableDefinition.full_path, 'w'),
                                 fieldnames=tableDefinition.table_def.columns,
                                 restval='', extrasaction='ignore',
                                 quotechar='"', quoting=csv.QUOTE_ALL)

        return _writer

    def create_writers(self):

        _resultTableMap = {'classifyText': ['documents', 'categories', 'errors'],
                           'extractDocumentSentiment': ['documents', 'sentences', 'errors'],
                           'extractEntities': ['documents', 'entities', 'mentions', 'errors'],
                           'extractEntitySentiment': ['documents', 'entities', 'mentions', 'errors'],
                           'extractSyntax': ['documents', 'sentences', 'tokens', 'errors']}

        _resultsTableColumn = {'documents': FIELDS_DOCUMENTS,
                               'sentences': FIELDS_SENTENCES,
                               'categories': FIELDS_CATEGORIES,
                               'tokens': FIELDS_TOKENS,
                               'entities': FIELDS_ENTITIES,
                               'mentions': FIELDS_MENTIONS,
                               'errors': FIELDS_ERRORS}

        _createdTables = []
        _createdTablesDef = []

        for method in self.paramMethods:

            _tables = _resultTableMap[method]

            for t in _tables:

                if t not in _createdTables:

                    logging.debug("Creating writer for %s." % t)

                    _tableDef = self._create_table_definition(t, _resultsTableColumn[t])
                    _writer = self._create_csv_writer(_tableDef)

                    if t == 'documents':

                        self.writerDocuments = _writer
                        self.writerDocuments.writeheader()

                    elif t == 'sentences':

                        self.writerSentences = _writer
                        self.writerSentences.writeheader()

                    elif t == 'categories':

                        self.writerCategories = _writer
                        self.writerCategories.writeheader()

                    elif t == 'tokens':

                        self.writerTokens = _writer
                        self.writerTokens.writeheader()

                    elif t == 'entities':

                        self.writerEntities = _writer
                        self.writerEntities.writeheader()

                    elif t == 'mentions':

                        self.writerMentions = _writer
                        self.writerMentions.writeheader()

                    elif t == 'errors':

                        self.writerErrors = _writer
                        self.writerErrors.writeheader()

                    _writer = None
                    _createdTables += [t]
                    _createdTablesDef += [_tableDef]

                else:

                    continue

        self.resultTableDefinitions = _createdTablesDef
        self.resultTableNames = _createdTables

    @staticmethod
    def _create_manifest_template(pk=[], incremental=True):

        return {'primary_key': pk, 'incremental': incremental}

    def create_manifests(self):

        for tableDef in self.resultTableDefinitions:

            if tableDef.table_def.name == 'errors':

                _manifest = self._create_manifest_template(pk=[], incremental=False)

            else:

                _manifest = self._create_manifest_template(pk=tableDef.table_def.pk)

            _path = tableDef.full_path + '.manifest'
            with open(_path, 'w') as file:

                json.dump(_manifest, file)
