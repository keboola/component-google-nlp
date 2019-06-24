The sample of the configuration, including input & output tables, can be found in the [component's repository](https://bitbucket.org/kds_consulting_team/kds-team.ex-google-nlp/src/master/component_config/sample-config/). In general, an input table and 3 parameters are required to configure the component.

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