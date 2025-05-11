import os
import logging
from pydataimport.services.file.file_service import read_json_file, write_json_file
from pydataimport.utils.common_util import gen_str_to_snake_case
from pydataimport.services.db.storage_service import get_sqlserver_py_datatype_map

# g_default_directory_path = "./app/dependencies/autoapi"
g_default_directory_path = "./assets"
g_datatype_map_identification_key = "_data_type_map"
g_datatype_map_temp_identification_key = g_datatype_map_identification_key+"_temp"
g_datatype_map_directory = "datatypemap"
g_datatype_map_temp_directory = "datatypemaptemplate"


def read_datatype_map_file(table_name):
    '''
    Read Datatype Map File
    '''
    datatype_map_file_name = table_name + g_datatype_map_identification_key
    datatype_map_file_path = g_default_directory_path + \
        os.sep + g_datatype_map_directory
    return read_json_file(datatype_map_file_name, datatype_map_file_path)


def write_datatype_map_file(table_name, datatype_map_dict):
    '''
    Write Datatype Map File
    '''
    datatype_map_file_name = table_name + g_datatype_map_identification_key
    datatype_map_file_path = g_default_directory_path + \
        os.sep + g_datatype_map_directory
    write_json_file(datatype_map_file_name,
                    datatype_map_dict, datatype_map_file_path)


def read_datatype_map_template_file(table_name):
    '''
    Read Datatype Map File
    '''
    datatype_map_file_name = table_name + g_datatype_map_temp_identification_key
    datatype_map_file_path = g_default_directory_path + \
        os.sep + g_datatype_map_temp_directory
    return read_json_file(datatype_map_file_name, datatype_map_file_path)


def write_datatype_map_template_file(table_name, datatype_map_dict):
    '''
    Write Datatype Map File
    '''
    datatype_map_file_name = table_name + g_datatype_map_temp_identification_key
    datatype_map_file_path = g_default_directory_path + \
        os.sep + g_datatype_map_temp_directory
    write_json_file(datatype_map_file_name,
                    datatype_map_dict, datatype_map_file_path)



def generate_temp_datatype_map_file(table_name, df):

    column_datatype_map = {}
    for col_name in df.columns:

        cell_value = df.at[0, col_name]
        '''Replace special characters from column name'''
        table_col_name = gen_str_to_snake_case(col_name)

        column_datatype_map[table_col_name] = {
            "column_name": col_name,
            "sample_value": str(cell_value),
            "py_datatype": "{}_py_datatype".format(table_col_name),
            "db_datatype": "{}_db_datatype".format(table_col_name)
        }
    write_datatype_map_template_file(table_name, column_datatype_map)


def consume_temp_datatype_map_file(table_name, df):
    stored_temp_map = read_datatype_map_template_file(table_name)

    if stored_temp_map is not None:
        sqlserver_py_datatype_map = get_sqlserver_py_datatype_map()

        is_missing_column_datatype = False
        for col_key in stored_temp_map:
            db_datatype = stored_temp_map[col_key]['db_datatype']
            if db_datatype != col_key+'_db_datatype':
                stored_temp_map[col_key]['py_datatype'] = sqlserver_py_datatype_map[db_datatype.split("(")[
                    0]]
            else:
                is_missing_column_datatype = True

        if not is_missing_column_datatype:
            write_datatype_map_file(table_name, stored_temp_map)
            return stored_temp_map

    return None


def get_column_datatype_map(table_name, df=None):
    # insert only
    # if not active_create:
    # Main Map File
    stored_map = read_datatype_map_file(table_name)
    # return full map
    if df is None:
        return stored_map if stored_map is not None else None

    # process temp Map File and create Map file
    if stored_map is None:
        # Temp Map File
        stored_map = consume_temp_datatype_map_file(table_name, df)

    if stored_map:
        # return Map only for available columns in data frame
        current_column_keys = [gen_str_to_snake_case(
            column_name) for column_name in df.columns]
        common_column_keys_map = {
            key: stored_map[key] for key in stored_map.keys() if key in current_column_keys}
        # common_column_keys = set(current_column_keys).intersection(stored_map.keys())
        # common_column_map = {key:stored_map[key] for key in common_column_keys}
        # stored_map = { col_key:stored_map[col_key] for col_key in stored_map.keys() if stored_map[col_key]["column_name"] in df.columns }
        return common_column_keys_map
    else:
        # Map and Temp Map, both Files are not available
        logging.info("No Datatype Map File Found")
        logging.info(
            f"Generating temporary Datatype Map File for {table_name}, Pls enter db_datatype there")
        generate_temp_datatype_map_file(table_name, df)
        return None
