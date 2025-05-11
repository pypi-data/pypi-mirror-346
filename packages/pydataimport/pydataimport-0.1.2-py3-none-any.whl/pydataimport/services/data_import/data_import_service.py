import logging
import traceback
import pandas as pd
import pydataimport.services.db.data_storage_service as dss
import pydataimport.services.db.storage_service as ss
import pydataimport.services.db.data_storage_query_service as dsqs
import pydataimport.services.db.datatype_service as dts
import pydataimport.services.file.file_service as fs
import pydataimport.services.log.log_service as ls
import pydataimport.services.fetch.data_fetch_service as dfs
import pydataimport.utils.data_utli as du
import pydataimport.config.db_config as db

OPERATION_MODE = {
        'DROP_OLD_CREATE_NEW': 'drop-old,create-new',
        'DROP_OLD_CREATE_NEW_BULK_INSERT': 'drop-old,create-new,bulk-insert',
        'BULK_INSERT': 'bulk-insert',
        'BULK_INSERT_DROP_ALL_OLD': 'bulk-insert,drop-all-old',
        'INSERT_NON_DUPLICATES': 'insert-non-duplicates',
        'SINGLE_INSERT': 'single-insert',
        'SINGLE_INSERT_DROP_ALL_OLD': 'single-insert,drop-all-old',
        'DROP_OLD_CREATE_NEW_SINGLE_INSERT': 'drop-old,create-new,single-insert'
    }


def has_insert_mode(operation_mode):
    for mode in operation_mode.split(','):
        if mode in ['bulk-insert', 'insert-non-duplicates', 'single-insert']:
            return True
    return False


def import_data(data_format, source_path, table_name, operation_mode="insert-non-duplicates", default_directory="", excel_sheet_name=0):

    OPERATION_MODES = operation_mode.split(",")
    # is_create = not not "drop-old" in OPERATION_MODES

    global g_default_directory_path
    if default_directory != "":
        g_default_directory_path = default_directory

    activity_log = {}

    # DATA INSERTION MODE - SO FETCH DATA FROM SOURCE and PROCESS
    if has_insert_mode(operation_mode):
        # fetch data from source
        df = dfs.fetch_data_from_src(data_format, source_path, excel_sheet_name)
        if df is None:
            logging.error(f"Data Fetch Failed, source: {source_path}")
            return
        
        logging.info(f"Data Fetch Success, records: {len(df)}")
        data = du.process_data(table_name, df)

        insert_query_feed = dsqs.get_insert_query_feed(table_name, df)

        if insert_query_feed is None or data is None:
            return
        logging.info(f"Data Processing Success, records: {len(data)}")
        

    with db.db_con() as conn:
        if "drop-old" in OPERATION_MODES:
            # drops the table if it exists
            activity_log["drop_table"] = dss.drop_table(conn, table_name)

        if "create-new" in OPERATION_MODES:
            create_table_query_feed = dsqs.get_create_table_query_feed(table_name)

            # creates new Table in Database
            activity_log["create_table"] = dss.create_table(conn, table_name, create_table_query_feed)
    
        if "bulk-insert" in OPERATION_MODES:
            # Dump available Bulk Data (without duplicate record check)
            activity_log["multi_insert"] = dss.dump_all_data(conn, table_name, insert_query_feed, data)
        elif "insert-non-duplicates" in OPERATION_MODES:
            # Insert available Bulk Data
            activity_log["single_insert"] = dss.safe_dump_data(conn, table_name, df, insert_query_feed, data)
        elif "single-insert" in OPERATION_MODES:
            # Insert available Data
            activity_log["single_insert"] = dss.dump_data(conn, table_name, df, insert_query_feed, data)

        # Delete all old data from table after new data insertion
        if "drop-all-old" in OPERATION_MODES:
            # Delete all old data from table
            activity_log["delete_all_old_data"] = dss.delete_all_old_data(conn, table_name)
        
    return activity_log