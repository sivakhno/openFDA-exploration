import glob

from tinydb import TinyDB

from .utils import get_logger

logger = get_logger(__name__)


def get_reactionmeddrapt(record):
    return ','.join([item['reactionmeddrapt'] for item in record['patient']['reaction']])


def get_drugindication(record):
    return ','.join([item['drugindication'] for item in record['patient']['drug']])


def get_generic_name(record):
    '''
    FDA provides common ontologies for generic names https://open.fda.gov/apis/openfda-fields/
    Here we are trying to return a common generic name from a set of records via sorting
    and returning the first in the sorted list
    '''
    return ','.join([sorted(item['openfda']['generic_name'])[0] for item in record['patient']['drug']])


def get_substance_name(record):
    return ','.join(
        [' '.join(item['openfda']['substance_name'])
         for item in record['patient']['drug']])


def get_activesubstance(record):
    return ','.join([item['activesubstance']['activesubstancename'] for item in record['patient']['drug']])


def get_all_generic_names(record):
    return ';'.join(
        [', '.join(item['openfda']['generic_name'])
              for item in record['patient']['drug']])


def get_occurcountry(record):
    return record['occurcountry']


def get_record_id(record):
    return record['safetyreportid']


def parser_base(inpath, custom_parser, raw_data_db_base, parsed_data_db_base):
    '''
    Extracts and saves information from raw openFDA records data using custom_parser. 
    :inpath: db directory
    :custom_parser: function specifying parsing rules
    :raw_data_db_base: base name for raw openFDA records data
    :parsed_data_db_base: base name for processed openFDA records data
    '''
    parser_name = custom_parser.__name__.replace('parse_', '')
    db_name = f'{inpath}/{parsed_data_db_base}_{parser_name}.json'
    logger.info(f'Writing to db {db_name}')
    db_processed = TinyDB(db_name)
    db_partitions = glob.glob(f'{inpath}/{raw_data_db_base}*.json')
    for db_partition in db_partitions:
        with TinyDB(db_partition) as db:
            sizedb = len(db)
            counter = 0
            skipped_records_counter = 0
            results_final = []
            for record in db:
                result_final = {}
                try:
                    custom_parser(result_final, record)
                except Exception:
                    skipped_records_counter += 1
                    continue
                if counter % 1000 == 0:
                    logger.info(f'Counter at position {counter} out of {sizedb} for db {db_partition}')
                counter += 1  
                results_final.append(result_final)
            db_processed.insert_multiple(results_final)
        logger.info(f'Skipped {skipped_records_counter} records, parsed {counter} records for db {db_partition}.')     
    db_processed.close()


def parse_all_records(result_final, record):
    result_final['reactionmeddrapt'] = get_reactionmeddrapt(record)
    result_final['drugindication'] = get_drugindication(record)
    result_final['generic_name'] = get_generic_name(record)
    result_final['activesubstancename'] = get_activesubstance(record)
    result_final['substance_name'] = get_substance_name(record)
    result_final['occurcountry'] = get_substance_name(record)
    result_final['id'] = get_record_id(record)


def parse_drugindication(result_final, record):
    result_final['reactionmeddrapt'] = get_reactionmeddrapt(record)
    result_final['drugindication'] = get_drugindication(record)
    result_final['id'] = get_record_id(record)


def parse_taken_together(result_final, record):
    result_final['generic_name'] = get_generic_name(record)
    result_final['id'] = get_record_id(record)


def parse_reaction_by_country(result_final, record):
    result_final['occurcountry'] = get_occurcountry(record)
    result_final['reactionmeddrapt'] = get_reactionmeddrapt(record)
    result_final['id'] = get_record_id(record)