import argparse
import sys
import multiprocessing as mp
import os
from functools import partial

from src.utils import get_date_periods, create_timestamped_folder
from src.api import retrieve_records_wrapper, \
     DATA_DB_DIR_BASE, RAW_DATA_DB_BASE, PARSED_DATA_DB_BASE, \
     DEFAULT_START, DEFAULT_END
from src.parser import parse_all_records, parse_drugindication, parser_base, \
     parse_taken_together, parse_reaction_by_country

_path = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_time_ranges', type=int, default=2) 
    parser.add_argument('--upload_to_s3', action='store_true', help='run on subset of data')
    parser.add_argument('--parse_from_crawled', action='store_true', help='parse previously saved records')
    parser.add_argument('--db_dir', help='parse previously saved records', required=False)

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f'Error {e} while parsing command line arguments.')
        parser.print_help()
        sys.exit(0)
        
    if args.parse_from_crawled and args.db_dir is None:
        parser.error('--parse_from_crawled requires --ldb_dir')

    n_cpus = max(mp.cpu_count(), 2)

    if not args.parse_from_crawled:
        date_processid_tuples, time_delata = get_date_periods(
            args.num_time_ranges, n_cpus, DEFAULT_START, DEFAULT_END)
        outpath = create_timestamped_folder(_path, DATA_DB_DIR_BASE)
        retrieve_records_wrapper_partial = partial(retrieve_records_wrapper, time_delata, outpath)
        with mp.Pool(processes=n_cpus) as pool:
            result = pool.starmap(retrieve_records_wrapper_partial, date_processid_tuples)
        sys.exit(0)

    else:
        parser_base(args.db_dir, parse_all_records, RAW_DATA_DB_BASE, PARSED_DATA_DB_BASE)
        parser_base(args.db_dir, parse_drugindication, RAW_DATA_DB_BASE, PARSED_DATA_DB_BASE)
        parser_base(args.db_dir, parse_taken_together, RAW_DATA_DB_BASE, PARSED_DATA_DB_BASE)
        parser_base(args.db_dir, parse_reaction_by_country, RAW_DATA_DB_BASE, PARSED_DATA_DB_BASE)
