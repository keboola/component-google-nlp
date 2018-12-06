import os
import logging
import pandas as pd
from service.analyzer \
    import analyze_entities, analyze_sentiment, analyze_syntax, get_native_encoding_type, analyze_entity_sentiment
from service.flattener import parse_syntax_res, parse_sentiment_res, parse_entity_res, parse_entity_sentiment_res


DEFAULT_TABLE_SOURCE = "/data/in/tables/"
DEFAULT_TABLE_DESTINATION = "/data/out/tables/"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")

logging.getLogger("googleapiclient").setLevel(logging.ERROR)


def request_analysis(a_type, key, record):
    input_text = record[1]
    if a_type == 'entities':
        result = analyze_entities(input_text, key, get_native_encoding_type())
        df_result = parse_entity_res(record, result)
    elif a_type == 'sentiment':
        result = analyze_sentiment(input_text, key, get_native_encoding_type())
        df_result = parse_sentiment_res(record, result)
    elif a_type == 'syntax':
        result = analyze_syntax(input_text, key, get_native_encoding_type())
        df_result = parse_syntax_res(record, result)
    elif a_type == 'entity_sentiment':
        result = analyze_entity_sentiment(input_text, key, get_native_encoding_type())
        df_result = parse_entity_sentiment_res(record, result)

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


def main(input_file_path, analysis_type, api_key):
    df = pd.read_csv(input_file_path)
    df = df[['id', 'query']]
    records = df.to_records(index=False)

    for r in records:
        logging.info("Analyzing: {} ...".format(r[1][:50]))
        df_result_d = request_analysis(analysis_type, api_key, r)
        for df_result_k in df_result_d:
            output(df_result_k, df_result_d[df_result_k])
