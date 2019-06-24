# Google NLP

## Overview

The Google Natual Language API allows users to utilize powerful pre-trained NLP models to understand various language features such as sentiment, entities and mentions, content and syntax. The component utilizes the API to send text features and retrieves desired analysis.

The Cloud Natural Language API is a paid service maintained by Google and is subject to [Google Cloud's Terms & Conditions](https://cloud.google.com/terms/). 

The information about pricing can be found on [Google's support forums](https://cloud.google.com/natural-language/pricing). The API currently supports [these methods and languages](https://cloud.google.com/natural-language/docs/languages).

#### Useful links

If you are new to the natural language processing or are unsure about the meaning of outputted values, the following guides might clear up some of the confusion:

- [Natual Language API Basics](https://cloud.google.com/natural-language/docs/basics)
- [Morphology & Dependency Trees](https://cloud.google.com/natural-language/docs/morphology)
- [HTTP status and error codes for JSON](https://cloud.google.com/storage/docs/json_api/v1/status-codes)

## Requirements

The component requires valid Google Cloud API token with Natural Language API allowed. The API token is subject to [limits](https://cloud.google.com/natural-language/quotas) thus it is important to set the correct daily limits. To overcome the 100 second limits, the application uses exponential backoff with 10 retries. In case, the retries are unsuccessful (i.e. daily limit is reached), the component fails.

## Supported languages & methods

The component supports all of the [languages supported by the API](https://cloud.google.com/natural-language/docs/languages). If the (detected) language isn't supported, the request will be cancelled, the document is skipped and no output is produced for it. All of the language errors are outputted to `errors` table.

The component currently supports following methods:

- `analyzeEntities` - entity analysis,
- `analyzeEntitySentiment` - entity sentiment analysis,
- `analyzeSentiment` - sentiment analysis,
- `analyzeSyntax` - syntactic analysis,
- `classifyText` - content classification.

Note: The component uses API v1. The list of all methods supported by the version is listed in [API reference](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents). Mind that, `annotateText` method is a wrapper for all other methods listed above and does not provide any new information. It is used in the component to bundle [all feature requests into a single API call](https://cloud.google.com/natural-language/docs/basics/#text-annotations).

If a new method is available and you'd like to see it, contact us at [support@keboola.com](mailto:support@keboola.com) or via support ticket.

---

#### Entity analysis (`analyzeEntities`)

The method inspects the document for known entities and returns [information about the entities](https://cloud.google.com/natural-language/docs/basics/#entity_analysis), such as their type, salience and mentions in the text. Moreover, if any metadata (e.g. address, phone number, famous person) is identified, the information on the subject is returned as well (e.g. full address, country code for the phone number, wikipedia article about the person). For more information about metadata, see the [`Entity` type documentation](https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity#type).

For each entity, a list of mentions is returned. The mentions list is always of length at least 1, i.e. each entity has at least one mention.

###### reference: [analyzeEntities](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeEntities), [entity](https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity)


#### Entity sentiment analysis (`analyzeEntitySentiment`)

The method returns the same analysis type as `analyzeEntities` method but adds sentiment analysis for each entity and mention in the text, thus [combining both entity and sentiment analysis](https://cloud.google.com/natural-language/docs/basics/#entity-sentiment-analysis). Note that, if both `analyzeEntities` and `analyzeEntitySentiment` methods are used, you will not be charged for both methods; only `analyzeEntitySentiment` will be utilized and billed.

###### reference: [analyzeEntitySentiment](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeEntitySentiment), [entity](https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity)

#### Sentiment analysis (`analyzeSentiment`)

The `analyzeSentiment` method inspects the document for [emotional opinion present within the text](https://cloud.google.com/natural-language/docs/basics/#sentiment_analysis) and magnitude of the opinion. The result is the overall attitude of the document (positive, neutral or negative) and of each sentence present within the document. Score and magnitude of the document and sentences can be interpreted according to [this guide](https://cloud.google.com/natural-language/docs/basics/#interpreting_sentiment_analysis_values).

###### reference: [analyzeSentiment](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeSentiment), [sentiment](https://cloud.google.com/natural-language/docs/reference/rest/v1/Sentiment)

#### Syntactic analysis (`analyzeSyntax`)

The syntactic analysis breaks up the documents into [sentences and extracts tokens (words)](https://cloud.google.com/natural-language/docs/basics/#syntactic_analysis) from the document. For each token, information about lemma, [part of the speech](https://cloud.google.com/natural-language/docs/reference/rest/v1/Token/#PartOfSpeech) and [depencency index](https://cloud.google.com/natural-language/docs/reference/rest/v1/Token/#DependencyEdge) is added using Cloud Natural Language API. For more information about how to interpret the values, refer to [Syntacting analysis](https://cloud.google.com/natural-language/docs/basics/#syntactic_analysis) guide and [Morphology & Dependency Trees](https://cloud.google.com/natural-language/docs/morphology) guide.

###### reference: [analyzeSyntax](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeSyntax), [token](https://cloud.google.com/natural-language/docs/reference/rest/v1/Token)

#### Content classification (`classifyText`)

The `classifyText` method analyzes the document and returns a list of [categories that apply to the text](https://cloud.google.com/natural-language/docs/basics/#content-classification) found in the document. For each category, a confidence level is provided as well as the name of the category. A complete list of all available categories can be found in [Categories section](https://cloud.google.com/natural-language/docs/categories) of API documentation. 

For successful content classification, the document needs to be of certain length (~ 20 words) and must not be too abstract. If the two conditions are not met, no categories are returned.

###### reference: [classifyText](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/classifyText), [ClassificationCategory](https://cloud.google.com/natural-language/docs/reference/rest/v1/ClassificationCategory)

## Input and Output

The sample of the configuration, including input & output tables, can be found in the [component's repository](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/component_config/sample-config/). In general, an input table and 3 parameters are required to configure the component.

### Parameters

All of the parameters listed in the section are required. If any of the parameters are not provided or an invalid value is provided, the component will fail. The API key is verified against Cloud API. The sample of the configuration file can be found [here](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/component_config/sample-config/config.json).

#### API Key (`#API_key`)

The API key can be obtained in the credentials section of the [Google Cloud Console](https://console.cloud.google.com/apis/credentials). The API key must have Cloud Natural Language API allowed, otherwise, requests will not be authorized. The [limits](https://cloud.google.com/natural-language/quotas) for the token must be specified according to your needs.

#### Analysis Type (`analysis_type`)

A list of methods to be used in the analysis. Supported methods are:

- `analyzeEntities`
- `analyzeEntitySentiment`
- `analyzeSentiment`
- `analyzeSyntax`
- `classifyText`

#### Input Type (`input_type`)

A string represing the type of text inputted into `text` column in the input table. Must be one of the two:

- `PLAIN_TEXT` - a plain text; consumes less characters,
- `HTML` - a html text; consumes more characters as all html tags counted in as well.

### Input table

The input table must contain two required columns `id` and `text` and might contain an optional column `sourceLanguage`. All extra columns are ignored; an exception is raised if any of the required columns is missing. The sample of the table can be found in the [repository](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/component_config/sample-config/in/tables/test.csv).

The column descriptions are:

- `id` (required) - ID of a document; make sure the ID is unique as the output data is loaded incrementally,
- `text` (required) - document to be analyzed; might contain html tags if `input_type=HTML` is specified
- `sourceLanguage` (optional) - an [ISO-639-1 language identifier](https://cloud.google.com/translate/docs/languages) of the source language; see section *Supported languages & methods*; if left empty, the API automatically detects the language.

The input table, therefore, might take the following form:

| id 	| text 	| sourceLanguage 	| otherColumn 	|
|----	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|----------------	|-------------	|
| 1 	| Keboola brings data engineering and data analytics together on one single platform that anyone can use. One click managed infrastructure, data hub, user provisioning, process automation - all rolled into one platform. Call us at +420 739 632 821 or visit us at Křižíkova 488/115 Prague 8 186 00 	| en 	| foo 	|
| 2 	| Google, headquartered in Mountain View (1600 Amphitheatre Pkwy,  Mountain View, CA 940430), unveiled the new Android phone for  $799 at the Consumer Electronic Show. Sundar Pichai said in his  keynote that users love their new Android phones. 	|  	| bar 	|
| 3 	| This text is too short to use classifyContent method. 	|  	| foobar 	|

### Data splitting

The output of the API is, usually, a quite complicated object, that needs to be parsed and split into multiple tables. For example, the full response body, with all methods used, for the sentence

```
Keboola brings data engineering and data analytics together on one single platform that anyone can use. One click managed infrastructure, data hub, user provisioning, process automation - all rolled into one platform. Call us at +420 739 632 821 or visit us at Křižíkova 488/115 Prague 8 186 00
```

is over 2000 lines long; it can be viewed in [sample examples](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/example/sample-response.json). If all methods are used, the result is split into 7 tables:

- `documents`,
- `errors`,
- `sentences`,
- `entities`,
- `mentions`,
- `tokens`,
- `categories`.

All of the tables, except `errors` are loaded incrementally and contain a unique identifier, which is based mainly on document's `id`.

#### Primary keys and relationships

In the following sections, each output table will be discussed, its PK creation process explained and relationship to other tables touched on.

##### `documents`

Contains information about documents, their language and if applicable, sentiment values of the whole document. The table is considered to be a root table, i.e. all other tables are referencing to this table. 

As the primary key, the provided identifier of each document is used. If the NLP analysis fails, for whatever reason, the failed document is not recorded in the table; instead it appears in the `errors` table. If method `analyzeSentiment` is not used, the columns containing information about sentiment values are left empty.

###### Result of: `analyzeEntities`, `analyzeEntitySentiment`, `analyzeSentiment`, `analyzeSyntax`, `classifyText`

##### `errors`

Contains information about warnings and errors sustained during the run of the component. All messages are referencing to `documents` table via column `documentId`.

All of the records contain category of the error, possible value are:

- `categoryError` - error when no category could be identified,
- `nlpError` - error related to Cloud Natural Language API,
- `emptyDocumentError` - error related to document being empty.

If `categoryError` occurs, the process for the document will be retried without the `classifyText` method, unless there are no other methods to be processed. The `nlpError` marks language errors, i.e. unsupported languages for some or all entities, no retry is tried. `emptyDocumentError` causes the process to skip over the document. Additionally, each row contains the message returned by the API for better understanding.

The table is **not** loaded incrementally.

###### Result of: `analyzeEntities`, `analyzeEntitySentiment`, `analyzeSentiment`, `analyzeSyntax`, `classifyText`

##### `sentences`

A child table to `documents`; each child is referenced back via `documentId` column and has a unique identifier, which is created as

```
sentenceId = md5(documentId + '|' + sentence.content + '|' + sentence.beginOffset)
```

where `md5()` is a hashing function, `sentence.content` is a textual representation of the sentence (API output) and `sentence.beginOffset` is a character offset to the start of the sentence (API output).

The table contains information about sentences present in the document. If `analyzeSentiment` is used, the table also contains sentiment value for each of the sentences. In addition to standard API output, column `index` is added manually and marks position of sentence in the document. The indexing columns starts at 0.

###### Result of: `analyzeSentiment`, `analyzeSyntax`

##### `entities`

The table `entities` contains information about proper entities present in the document. Each entity is a child of a document (referenced via `documentId`) and has a unique `entityId` created as

```
entityId = md5(`documentId` + '|' + entity.name)
```

where `entity.name` is the textual representation of the entity. If `analyzeEntitySentiment` method is used, also contains information about sentiment values, otherwise the columns are left empty. 

The table is a parent table to `mentions`.

###### Result of: `analyzeEntities`, `analyzeEntitySentiment`

##### `mentions`

A child table to `entities`, related via `entityId` column. Each entity has one or more mentions, words, which are referencing said entity. Textual representations of mentions for an entity might be duplicate if the same word is used to reference back to the entity, though they are different mentions. 

The column `mentionId`, a primary key, is created as a combination of

```
mentionId = md5(entityId + '|' + mention.content + '|' + mention.beginOffset)
```

where `entityId` is a parent entity, `mention.content` is a word representation of the mention (API output) and `mention.beginOffset` is a character offset of the mention. 

The effect of using `analyzeEntitySentiment` is the same as for `entities` table.

###### Result of: `analyzeEntities`, `analyzeEntitySentiment`

##### `tokens`

A child table to `documents` (foreign key `documentId`), which captures information about tokens in a document. The unique identifier is created by

```
tokenId = md5(documentId + '|' + token.content + '|' + token.beginOffset + '|' + index)
```

where `token.content` is a token name (word), `token.beginOffset` is the character offset of the token in the document and `index` is a tokens position in the document. The index starts at 0 and is useful for creating dependency trees with `token.dependencyEdge` parameters.

###### Result of: `analyzeSyntax`

##### `categories`

Referencing back to `documents` via `documentId` column, the `categories` table contains information about catefories identified using `classifyText` method. The `categoryDocumentId` is a concatenation of category's name and `documentId`, i.e.

```
categoryDocumentId = md5(documentId + '|' + category.name)
```

where `category.name` is the name of the identified category (API output). Each document can have 0 or more categories.

###### Result of: `classifyText`

#### Column descriptions

Due to a high number of tables present in the dataset, the column descriptions will not be a part of this documentation. However, a great in-depth description is available in [Natual Language API Basics](https://cloud.google.com/natural-language/docs/basics) guide.

## Development

For development purposed the following `docker-compose` commands should be used:

```
docker-compose build dev
docker-compose run --rm dev
```

or 

```
docker-compose up
```