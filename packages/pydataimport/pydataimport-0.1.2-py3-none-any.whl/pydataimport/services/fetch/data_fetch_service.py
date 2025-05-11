import logging

import pandas as pd
from pydataimport.services.log.log_service import track_data_fetch


def fetch_data_from_src(data_format, source_path, excel_sheet_name=0):
    df = None
    with track_data_fetch(timeout=600.0):
        # Fetch data from source
        if data_format == "csv":
            df = pd.read_csv(source_path)
        elif data_format == "excel":
            df = pd.read_excel(
                source_path, sheet_name=excel_sheet_name)  # , index_col=0)
        elif data_format == "json":
            df = pd.read_json(source_path)
        elif data_format == "dataframe" and isinstance(source_path, pd.DataFrame):
            df = source_path
        else:
            logging.error("Data Fetching from source Error")

    return df

