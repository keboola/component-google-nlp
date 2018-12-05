
import pandas as pd
import hashlib


def _hash_id(query_text):
    return hashlib.md5(query_text.encode('utf-8')).hexdigest()


def _add_pk_col(df, query_text):
    df['query_text'] = query_text
    df['query_id'] = _hash_id(query_text)
    return df


def parse_syntax_res(query_text, json_obj):

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
        dependency_edge_head_token_index = t.get('dependencyEdge').get('headTokenIndex')
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

    df_sentences = _add_pk_col(df_sentences, query_text)
    df_tokens = _add_pk_col(df_tokens, query_text)

    return {
        "sentences": df_sentences,
        "tokens": df_tokens
    }


# this handles 1 HTTP response
def parse_sentiment_res(query_text, json_obj):

    d_magnitude = json_obj.get('documentSentiment').get('magnitude')
    d_score = json_obj.get('documentSentiment').get('score')
    language = json_obj.get('documentSentiment').get('language')

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

    df_document_sentiment = _add_pk_col(df_document_sentiment, query_text)
    df_sentence_sentiments = _add_pk_col(df_sentence_sentiments, query_text)

    return {
        "document_sentiment": df_document_sentiment,
        "sentence_sentiments": df_sentence_sentiments
    }


# this handles 1 HTTP response = 1 text
def parse_entity_res(query_text, json_obj):
    entities = []
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

        mentions = e.get('mentions')

        for m in mentions:
            text = m.get('text')
            if text:
                content = metadata.get('content')
                begin_offset = metadata.get('beginOffset')
            else:
                content = None
                begin_offset = None
            m_type = m.get('type')
            mentions.append({
                'content': content,
                'beginOffset': begin_offset,
                'type': m_type
            })

    df_entities = pd.DataFrame.from_records(entities)
    df_mentions = pd.DataFrame.from_records(mentions)

    df_entities = _add_pk_col(df_entities, query_text)
    df_mentions = _add_pk_col(df_mentions, query_text)

    return {
        "entities": df_entities,
        "mentions": df_mentions
    }
