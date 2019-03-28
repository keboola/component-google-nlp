import os
import logging
import pandas as pd
import json
import re
import csv
from googleapiclient.errors import HttpError
from service.analyzer \
    import analyze_entities, analyze_sentiment, analyze_syntax, get_native_encoding_type, analyze_entity_sentiment
from service.flattener import parse_syntax_res, parse_sentiment_res, parse_entity_res, parse_entity_sentiment_res

ERR_HEADER = ['query_id', 'text', 'lang']

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
        result = analyze_entity_sentiment(
            input_text, key, get_native_encoding_type())
        df_result = parse_entity_sentiment_res(record, result)

    return df_result


def output(filename, data, out_folder):
    dest = os.path.join(out_folder, filename + ".csv")

    if os.path.isfile(dest):
        with open(dest, 'a') as b:
            data.to_csv(b, index=False, header=False)
        b.close()
    else:
        with open(dest, 'w+') as b:
            data.to_csv(b, index=False, header=True)
        b.close()


def main(input_file_path, analysis_type, api_key, out_folder):
    df = pd.read_csv(input_file_path)
    cols = df.columns.values
    msg = """Please prepare all your input tables with the 2 columns below:
    - id: the original ID column in your raw table, this is only for you to have a reference key
    - text: the column of texts you want to analyze Other columns in the tables will be omitted."""
    if not ('id' in cols) or not ('text' in cols):
        raise ValueError(msg)

    df = df[['id', 'text']]
    records = df.to_records(index=False)
    with open(os.path.join(out_folder, 'lang_errors.csv'), 'w+', newline='') as lang_errs:
        err_writer = csv.writer(lang_errs)
        err_writer.writerow(ERR_HEADER)
        for r in records:
            df_result_d = {}
            logging.info("Analyzing: {} ...".format(r[1][:50]))
            try:
                df_result_d = request_analysis(analysis_type, api_key, r)
            except HttpError as e:
                # ln = 'N/A'
                if json.loads(e.content).get('error', '').get('error', '').get('reason', '').find('keyInvalid') > 0:
                    raise ValueError("The API Key is invalid")
                elif json.loads(e.content).get('error', '').get('message', '').find(
                        'not supported for entity analysis.') > 0:  # noqa
                    err = json.loads(e.content)
                    ln = _get_language_from_error(err['error']['message'])
                    # write error output
                    err_writer.writerow(
                        [r[0], err['error']['message'], ln])

                    logging.error(err['error']['message'])

            for df_result_k in df_result_d:
                output(df_result_k, df_result_d[df_result_k], out_folder)


def _get_language_from_error(error_text):
    m = re.search(
        'The language (.*) is not supported for entity analysis.', error_text)
    return m.group(1)
