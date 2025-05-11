import numpy as np
import pandas as pd
import re
from datetime import datetime


def date_str(date_to_convert):
    # Format the date and time
    return date_to_convert.strftime("%Y-%m-%d")# %H:%M:%S")

def date_str_now():
    return date_str(datetime.now())


def drop_end_symbol(strg, symbol_count=1):
    if type(strg) is str:
        return strg[0:-1*symbol_count]
    else:
        return strg


def is_missing_value(val):
    return pd.isnull(val) or val is None or val == "" or val == "NULL" \
        or val == "null" or val == "NAN" or val == "nan" \
        or val == "NaN" or val == "Nan" \
        or (isinstance(val, (int, float, bool, complex)) and (np.isnan(val) or np.isinf(val)))\
        # or (isinstance(val, datetime.datetime) and np.isnat(val))
    # (isinstance(val, datetime) and np.isnat(val))


def validate_params():
    pass


def old_gen_str_to_snake_case(strg):
    '''Replave special characters from column name'''
    table_col_name = strg
    SPECIAL_CHARS = "!@  # $%^&*()-+={}[]:;'\"?., /\u00b3"
    for sc in SPECIAL_CHARS:
        table_col_name = table_col_name.replace(sc, "_")
    return table_col_name.lower()


def gen_str_to_snake_case(strg):
    '''Replave special characters from column name'''
    new_strg = re.sub("[^a-zA-Z_0-9]", "_", strg)
    return new_strg.lower()


def percent(val, total):
    return (val/total)*100

def is_percent_div_by(div_by, val, total):
    return percent(val, total) % div_by == 0