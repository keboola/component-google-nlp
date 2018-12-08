import pandas as pd


def _add_pk_col(df, record):
    # df['query_text'] = record[1]
    df['query_id'] = record[0]
    return df


def parse_syntax_res(record, json_obj):

    sentences = []
    tokens = []

    sentences_raw = json_obj.get('sentences')
    tokens_raw = json_obj.get('tokens')

    for s in sentences_raw:
        s_content = s.get('text').get('content')
        s_begin_offset = s.get('text').get('beginOffset')
        sentences.append({
            'content': s_content,
            'beginOffset': s_begin_offset
        })

    for t in tokens_raw:
        t_content = t.get('text').get('content')
        t_begin_offset = t.get('text').get('beginOffset')
        part_of_speech_tag = t.get('partOfSpeech').get('tag')
        part_of_speech_aspect = t.get('partOfSpeech').get('aspect')
        part_of_speech_case = t.get('partOfSpeech').get('case')
        part_of_speech_form = t.get('partOfSpeech').get('form')
        part_of_speech_gender = t.get('partOfSpeech').get('gender')
        part_of_speech_mood = t.get('partOfSpeech').get('mood')
        part_of_speech_number = t.get('partOfSpeech').get('number')
        part_of_speech_person = t.get('partOfSpeech').get('person')
        part_of_speech_proper = t.get('partOfSpeech').get('proper')
        part_of_speech_reciprocity = t.get('partOfSpeech').get('reciprocity')
        part_of_speech_tense = t.get('partOfSpeech').get('tense')
        part_of_speech_voice = t.get('partOfSpeech').get('voice')
        dependency_edge_head_token_index = t.get(
            'dependencyEdge').get('headTokenIndex')
        dependency_edge_label = t.get('dependencyEdge').get('label')
        lemma = t.get('lemma')
        tokens.append({
            'content': t_content,
            'beginOffset': t_begin_offset,
            'part_of_speech_tag': part_of_speech_tag,
            'part_of_speech_aspect': part_of_speech_aspect,
            'part_of_speech_case': part_of_speech_case,
            'part_of_speech_form': part_of_speech_form,
            'part_of_speech_gender': part_of_speech_gender,
            'part_of_speech_mood': part_of_speech_mood,
            'part_of_speech_number': part_of_speech_number,
            'part_of_speech_person': part_of_speech_person,
            'part_of_speech_proper': part_of_speech_proper,
            'part_of_speech_reciprocity': part_of_speech_reciprocity,
            'part_of_speech_tense': part_of_speech_tense,
            'part_of_speech_voice': part_of_speech_voice,
            'dependency_edge_head_token_index': dependency_edge_head_token_index,
            'dependency_edge_label': dependency_edge_label,
            'lemma': lemma
        })

    df_sentences = pd.DataFrame.from_records(sentences)
    df_tokens = pd.DataFrame.from_records(tokens)

    df_sentences = _add_pk_col(df_sentences, record)
    df_tokens = _add_pk_col(df_tokens, record)

    return {
        "sentences": df_sentences,
        "tokens": df_tokens
    }


# this handles 1 HTTP response
def parse_sentiment_res(record, json_obj):

    d_magnitude = json_obj.get('documentSentiment').get('magnitude')
    d_score = json_obj.get('documentSentiment').get('score')
    language = json_obj.get('language')

    document_sentiment = [{
        'magnitude': d_magnitude,
        'score': d_score,
        'language': language
    }]

    sentences_raw = json_obj.get('sentences')
    sentence_sentiments = []

    for s in sentences_raw:
        content = s.get("text").get("content")
        begin_offset = s.get("text").get("beginOffset")
        magnitude = s.get("sentiment").get("magnitude")
        score = s.get("sentiment").get("score")
        sentence_sentiments.append({
            'content': content,
            'beginOffset': begin_offset,
            'magnitude': magnitude,
            'score': score
        })

    df_document_sentiment = pd.DataFrame.from_records(document_sentiment)
    df_sentence_sentiments = pd.DataFrame.from_records(sentence_sentiments)

    df_document_sentiment = _add_pk_col(df_document_sentiment, record)
    df_sentence_sentiments = _add_pk_col(df_sentence_sentiments, record)

    return {
        "document_sentiment": df_document_sentiment,
        "sentence_sentiments": df_sentence_sentiments
    }


# this handles 1 HTTP response = 1 text
def parse_entity_res(record, json_obj):
    entities = []
    language = json_obj.get('language')
    entities_raw = json_obj.get('entities')
    mentions = []

    for e in entities_raw:
        name = e.get('name')
        e_type = e.get('type')
        salience = e.get('salience')
        metadata = e.get('metadata')
        if metadata:
            mid = metadata.get('mid')
            wikipedia_url = metadata.get('wikipedia_url')
        else:
            mid = None
            wikipedia_url = None

        entities.append({
            'name': name,
            'type': e_type,
            'salience': salience,
            'metadata_mid': mid,
            'metadata_wikipedia_url': wikipedia_url
        })

        mentions_raw = e.get('mentions')

        for m in mentions_raw:
            text = m.get('text')
            if text:
                content = text.get('content')
                begin_offset = text.get('beginOffset')
            else:
                content = None
                begin_offset = None
            m_type = m.get('type')
            mentions.append({
                'entity_name': name,
                'entity_type': e_type,
                'content': content,
                'beginOffset': begin_offset,
                'type': m_type
            })

    df_entities = pd.DataFrame.from_records(entities)
    df_mentions = pd.DataFrame.from_records(mentions)

    df_entities = _add_pk_col(df_entities, record)
    df_mentions = _add_pk_col(df_mentions, record)

    df_entities['language'] = language
    df_mentions['language'] = language

    return {
        "entities": df_entities,
        "mentions": df_mentions
    }


# this handles 1 HTTP response = 1 text
def parse_entity_sentiment_res(record, json_obj):
    entities = []
    entities_raw = json_obj.get('entities')
    language = json_obj.get('language')
    mentions = []

    for e in entities_raw:
        name = e.get('name')
        e_type = e.get('type')
        salience = e.get('salience')
        sentiment = e.get('sentiment')
        if sentiment:
            magnitude = sentiment.get('magnitude')
            score = sentiment.get('score')
        else:
            magnitude = None
            score = None

        metadata = e.get('metadata')
        if metadata:
            mid = metadata.get('mid')
            wikipedia_url = metadata.get('wikipedia_url')
        else:
            mid = None
            wikipedia_url = None

        entities.append({
            'name': name,
            'type': e_type,
            'salience': salience,
            'metadata_mid': mid,
            'metadata_wikipedia_url': wikipedia_url,
            'sentiment_magnitude': magnitude,
            'sentiment_score': score
        })

        mentions_raw = e.get('mentions')
        for m in mentions_raw:
            text = m.get('text')
            if text:
                content = text.get('content')
                begin_offset = text.get('beginOffset')
            else:
                content = None
                begin_offset = None

            m_sentiment = m.get('sentiment')
            if m_sentiment:
                m_magnitude = m_sentiment.get('magnitude')
                m_score = m_sentiment.get('score')
            else:
                m_magnitude = None
                m_score = None
            m_type = m.get('type')
            mentions.append({
                'entity_name': name,
                'entity_type': e_type,
                'content': content,
                'beginOffset': begin_offset,
                'type': m_type,
                'sentiment_magnitude': m_magnitude,
                'sentiment_score': m_score
            })

    df_entities = pd.DataFrame.from_records(entities)
    df_mentions = pd.DataFrame.from_records(mentions)

    df_entities = _add_pk_col(df_entities, record)
    df_mentions = _add_pk_col(df_mentions, record)

    df_entities['language'] = language
    df_mentions['language'] = language

    return {
        "entities_sentiment": df_entities,
        "mentions_sentiment": df_mentions
    }
