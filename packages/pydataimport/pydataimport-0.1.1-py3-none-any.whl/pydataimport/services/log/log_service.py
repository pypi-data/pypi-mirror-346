import numpy as np
import pandas as pd
import datetime
import time
import re
import logging
import socket
from pathlib import Path
from urllib.parse import quote_plus
import traceback
import pydataimport.services.file.file_service as fs
import contextlib
import time

LOGS_DIRECTORY = "./assets/logs"

@contextlib.contextmanager
def track_script_runtime():
    script_start_time = time.perf_counter()
    log_format = "[%(levelname)s]:%(asctime)s:%(filename)s:%(lineno)5s:%(funcName)s()\n%(message)s"
    # log_format = '[%(levelname)s] %(asctime)s %(message)s'
    fs.check_if_dir_exists(directory_path=LOGS_DIRECTORY)
    logging.basicConfig(level=logging.INFO, format=log_format, filename=LOGS_DIRECTORY+'/import_data_info.log', filemode='w')
    logging.info("---- Script Execution Started--------------------------------------------------------")
    
    yield

    script_end_time = time.perf_counter()
    script_runtime = script_end_time - script_start_time
    logging.info(f"---- Ecript Ends--(RT: {script_runtime} secs) ---------------------------------------")


@contextlib.contextmanager
def track_api_import(api_source, table_name, excel_sheet_name):
    logging.info(f">>>>>>>>>>>>>>>>> Processing API >>>>>>>>>>>>>>>>>")
    logging.debug("API Source: %s", api_source)
    logging.debug("Table Name: %s", table_name)
    logging.debug("Excel Sheet Name: %s", excel_sheet_name)

    '''Imports data from api and dumps it in to DB'''
    start_time = time.perf_counter()

    yield

    end_time = time.perf_counter()

    logging.info(f"Total time taken is {end_time-start_time} sec, to import data from {api_source} to {table_name}")
   

@contextlib.contextmanager
def track_data_fetch(timeout):
    try:
        timeout_before = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        data_fetch_start_time = time.perf_counter()
        
        yield

        data_fetch_end_time = time.perf_counter()
        data_fetch_time = data_fetch_end_time - data_fetch_start_time
        
        logging.info(f"Data Fetching from source Success, Time taken: {data_fetch_time} secs")
    except Exception as e:
        logging.error("Data Fetching from source Error")
        logging.error(f"Data Fetching Error: {e}")
    finally:
        socket.setdefaulttimeout(timeout_before)

