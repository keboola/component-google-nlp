## Google Cloud Natural Language 
This Extractor supports 4 types of NLP analysis 


###Language Support:
- [The languages Cloud Natural Language API currently support.](https://cloud.google.com/natural-language/docs/languages)

###Configuration Parameters:
- `API Key`: Users need to have their own API keys. API requests 
- `Analysis Type`: Choose between entity sentiment, entities, sentiment or syntax.
- Input Mapping: The input table structure requires the users to prepare a table contains the 2 following columns:
    1. `id`: The ID used in the original raw input table. The only purpose of this field is for users to link the NLP result back to the context.
    2. `text`: The text to be analyzed. It can be an article, a paragraph, a sentence or a word.



###Output:

#####Sentiment Analysis:
- Sentiment analysis scores each documents at 2 levels and returns 2 tables: `document_sentiment` & `sentence_sentimenet`


- Document Sentiment

|language|magnitude|score|query_id|
|---|---|---|---|
|en|2.5|0.6|user_review_12345|
|fr|0.6|0.6|user_review_12346|

- Sentence Sentiment
|beginOffset|content|magnitude|score|query_id|



- The 2 major metrics of sentiments are:
    1. `score`: How "positive" is the emotion presented in the document.
    2. `magnitude`: How "much" emotion is present within the document.
-It is recommended to define a threshold that works for you. A rule of thumb is scores greater than 0.25 can be considered as "Clearly Positive"; scores less than -0.25 can be considered as "Clearly Negative"; scores between the thresholds represent neutral emotions. 



Pipeline:
- run multiple types of analysis in one configuration.
