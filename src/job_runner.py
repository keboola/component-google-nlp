import os
import logging
import pandas as pd
from service.analyzer import analyze_entities, analyze_sentiment, analyze_syntax, get_native_encoding_type
from service.flattener import parse_syntax_res, parse_sentiment_res, parse_entity_res


DEFAULT_TABLE_SOURCE = "/data/in/tables/"
DEFAULT_TABLE_DESTINATION = "/data/out/tables/"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")


def request_analysis(a_type, key, input_text):

    if a_type == 'entities':
        result = analyze_entities(input_text, key, get_native_encoding_type())
        df_result = parse_entity_res(input_text, result)
    elif a_type == 'sentiment':
        result = analyze_sentiment(input_text, key, get_native_encoding_type())
        df_result = parse_sentiment_res(input_text, result)
    elif a_type == 'syntax':
        result = analyze_syntax(input_text, key, get_native_encoding_type())
        df_result = parse_syntax_res(input_text, result)

    return df_result


def output(filename, data):

    dest = DEFAULT_TABLE_DESTINATION + filename + ".csv"

    if os.path.isfile(dest):
        with open(dest, 'a') as b:
            data.to_csv(b, index=False, header=False)
        b.close()
    else:
        with open(dest, 'w+') as b:
            data.to_csv(b, index=False, header=True)
        b.close()


def main(input_file_path, seleted_column, analysis_type, api_key):

    df = pd.read_csv(input_file_path)
    queries = df[seleted_column]

    for q in queries:
        df_result_d = request_analysis(analysis_type, api_key, q)
        for df_result_k in df_result_d:
            output(df_result_k, df_result_d[df_result_k])

        break
