# Google NLP

**Full documentation available [here](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/README.md)!**

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