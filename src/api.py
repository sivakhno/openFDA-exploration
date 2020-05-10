import requests
import json
import time
import os
import logging
import sys

from tinydb import TinyDB
from .utils import get_logger

logger = get_logger(__name__)

REQUESTS_PER_MINUTE = 200
REQUEST_DURATION = 60.0/REQUESTS_PER_MINUTE
RECORDS_PER_REQUEST_LIMIT = 100
SKIP_VALUE_LIMIT = 25000
RAW_DATA_DB_BASE = 'db_raw'
PARSED_DATA_DB_BASE = 'db_parsed'
DATA_DB_DIR_BASE = 'db_dir'
DEFAULT_START = '1/1/2014'
DEFAULT_END = '1/1/2020'

_path = os.path.dirname(os.path.abspath(__file__))
gh_session = requests.Session()


def get_num_api_keys(api_keys_file=f'{_path}/../data/api_keys.txt'):
    '''
    Returns number of API keys in db.
    :api_keys_file: path to the file with API keys
    '''
    with open(api_keys_file, 'r') as api_key_filehandle:
        return len(api_key_filehandle.read().splitlines())


def count_records(name, api_key):
    '''
    Counts number of records for a given openFDA field.
    :api_keys_file: openFDA field
    :api_keys_file: API key
    '''
    logging.debug(f'counting number of records in field {name}')
    repos_url = f'https://api.fda.gov/drug/event.json?api_key={api_key}&count={name}'
    data = json.loads(gh_session.get(url=repos_url).text)
    try:
        results = data['results']
    except KeyError as e:
        logger.error(f'Error {e} when accessing results for field {name}')
        sys.exit(1)
    return results


def total_counts_records(name, api_key):
    '''
    Counts total number of records for a given openFDA field.
    :name: openFDA field
    :api_key: API key
    '''
    fields = count_records(name, api_key)
    try:
        results = sum([field['count'] for field in fields])
    except KeyError as e:
        logger.error(f'Error {e} when accessing results for item {field}')
        sys.exit(1)
    return results


def get_api_key(num_process, api_keys_file=f'{_path}/../data/api_keys.txt'):
    '''
    Returns API key for line num_process of api_keys_file
    TODO: check for index within bounds
    :num_process: openFDA field
    :api_keys_file: path to the file with API keys
    '''
    with open(api_keys_file, 'r') as api_key_filehandle:
        api_keys = api_key_filehandle.read().splitlines()
    return api_keys[num_process]


def retrieve_records(db, api_key, size, start_date, end_date, skip_value_limit, process_index):
    '''
    Returns API key for line num_process of api_keys_file
    :db: db connection
    :api_key: API key
    :size: openFDA API limit parameter
    :start_date: start date for openFDA date query of the form %Y%m%d
    :end_date: end date for openFDA date query of the form %Y%m%d
    :skip_value_limit openFDA max skip parameter value
    :process_index index of the multiprocessing lib process
    '''
    skip = 0
    date_range_query = f'search=receivedate:[{start_date}+TO+{end_date}]'
    while size + skip < skip_value_limit:
            repos_url = f'https://api.fda.gov/drug/event.json?api_key={api_key}&{date_range_query}&limit={size}&skip={skip}'
            try:
                data = json.loads(gh_session.get(url=repos_url).text)
            except Exception as e:
                logger.error(f'Error {e} executing request {repos_url}.') 
                continue
            try:
                results = data['results']
            except KeyError as e:
                logger.error(f'Error {e} when accessing results field using query {repos_url}.')
                continue
            try:
                db.insert_multiple(results)
            except Exception as e:
                logger.error(f'Error {e} writing  records.')
                sys.exit()
                continue
            skip += size
            if skip % 1000 == 0:
                logger.info(f'Skip at position {skip} for process {process_index}')
            time.sleep(REQUEST_DURATION) 


def retrieve_records_wrapper(time_delta, outpath, start_date, process_index):
    with TinyDB(f'{outpath}/{RAW_DATA_DB_BASE}{process_index}.json') as db:
        '''
        Wrapper pre-processing information for retrieve_records
        :time_delta: time delta for openFDA date query
        :outpath: location of db folder
        :start_date: start date for openFDA date query
        :process_index: index of the multiprocessing lib process
        '''
        end_date_str = (start_date + time_delta).strftime('%Y%m%d')
        start_date_str = start_date.strftime('%Y%m%d')
        skip_value_limit = SKIP_VALUE_LIMIT
        size = RECORDS_PER_REQUEST_LIMIT
        api_key = get_api_key(process_index)
        logger.info(f'Processing date range {start_date_str}-{end_date_str} for process {process_index}')    
        retrieve_records(db, api_key, size, start_date_str, end_date_str, skip_value_limit, process_index)
