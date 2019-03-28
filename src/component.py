'''
Template Component main class.

'''

from kbc.env_handler import KBCEnvHandler
import logging
import job_runner
import sys

MANDATORY_PARS = ['#API_key', 'analysis_type']

APP_VERSION = '0.0.19'


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        KBCEnvHandler.__init__(self, MANDATORY_PARS)
        # override debug from config
        if(self.cfg_params.get('debug')):
            debug = True

        self.set_default_logger('DEBUG' if debug else 'INFO')
        logging.info('Running version %s', APP_VERSION)
        logging.info('Loading configuration...')

        try:
            self.validateConfig()
        except ValueError as e:
            logging.error(e)
            exit(1)

    def run(self, debug=False):
        '''
        Main execution code
        '''
        params = self.cfg_params # noqa
        api_key = params.get('#API_key')
        analysis_type = params.get('analysis_type')
        tables = self.configuration.get_input_tables()

        if not tables:
            raise Exception("No input table found, please specify the input table in the input mapping section")

        for t in tables:
            input_file_path = t["full_path"]
            job_runner.main(input_file_path, analysis_type, api_key)


"""
        Main entrypoint
"""
if __name__ == "__main__":
    comp = Component()
    comp.run()
