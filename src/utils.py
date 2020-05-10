import pandas as pd
import math
import datetime
import os
import logging


def get_date_processid_tuples(periods, n_cpus):
    cpus = list(range(n_cpus)) * math.ceil(len(periods)/n_cpus)
    n_elements = min(len(periods), len(cpus))
    date_processid_tuples = [(periods[i], cpus[i]) for i in range(n_elements)]
    return date_processid_tuples


def get_date_periods(n_periods, n_cpus, start_date, end_date):
    start_date = start_date
    end_date = end_date
    periods = pd.date_range(start=start_date, end=end_date, periods=n_periods)
    time_delata = (periods[1]-periods[0])-pd.Timedelta(days=1)
    date_processid_tuples = get_date_processid_tuples(periods, n_cpus)
    return date_processid_tuples, time_delata


def create_timestamped_folder(base_path, base_dir):
    now = datetime.datetime.today()
    time_str = now.strftime('%Y-%m-%d-%H')
    folder_name = f'{base_dir}_{time_str}'
    dest_folder = os.path.join(base_path, folder_name)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    return dest_folder


def create_timestamped_file(base_file):
    now = datetime.datetime.today()
    time_str = now.strftime('%Y-%m-%d-%H')
    return f'{base_file}_{time_str}'  
 

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger