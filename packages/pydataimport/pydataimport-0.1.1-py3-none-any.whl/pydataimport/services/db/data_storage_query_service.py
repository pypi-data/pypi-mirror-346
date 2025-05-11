from pydataimport.services.db.datatype_service import get_column_datatype_map
from pydataimport.utils.common_util import drop_end_symbol
import datetime


def create_the_query_feed(table_name, df, active_create=False, is_complete_map=False):

    col_key_name_type_map = get_column_datatype_map(
        table_name, df)

    if col_key_name_type_map is None:
        return (None, None)

    # for index, row in df.iterrows():
    # single row iteration

    insert_query_feed = ",".join(col_key_name_type_map.keys())

    create_query_feed = None
    if active_create and is_complete_map:
        col_key_name_type_map = get_column_datatype_map(table_name)
        create_query_feed = ','.join(["{} {}".format(
            col_key, col_key_name_type_map[col_key]["db_datatype"]) for col_key in col_key_name_type_map])
    elif active_create:
        create_query_feed = ','.join(["{} {}".format(
            col_key, col_key_name_type_map[col_key]["db_datatype"]) for col_key in col_key_name_type_map])

    return (create_query_feed, insert_query_feed)


def get_create_table_query_feed(table_name):
    col_key_name_type_map = get_column_datatype_map(table_name)
    return ','.join(["[{}] {}".format(col_key, col_key_name_type_map[col_key]["db_datatype"]) for col_key in col_key_name_type_map])


def get_insert_query_feed(table_name, df=None):
    col_key_name_type_map = get_column_datatype_map(table_name, df)
    return ",".join(["[{}]".format(col_key_) for col_key_ in col_key_name_type_map.keys()]) if col_key_name_type_map is not None else None

def create_new_table_query(table_name, create_query_feed):
    return "CREATE TABLE {} ( id BIGINT PRIMARY KEY IDENTITY (1, 1), {}, created_at smalldatetime);".format(table_name, create_query_feed)


def create_insert_query(table_name, columns_name_query_feed):
    # ? string for query
    placeholders = ",".join("?" * len(columns_name_query_feed.split(",")))

    # import time stamp
    now = datetime.datetime.now()
    created_at_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    insert_query_temp = "INSERT INTO {} ({}, created_at) VALUES ({}, '{}')"

    insert_query = insert_query_temp.format(
        table_name, columns_name_query_feed, placeholders, created_at_timestamp)

    return insert_query


def create_complete_insert_query(table_name, columns_name_query_feed, values_list, created_at_timestamp):

    insert_query_temp = "INSERT INTO {} ({}, created_at) VALUES ({}, '{}')"

    queryfied_values = ",".join([queryfy_value(value)
                                 for value in values_list])
    complete_insert_query = insert_query_temp.format(
        table_name, columns_name_query_feed, queryfied_values, created_at_timestamp)

    return complete_insert_query


def create_select_query(table_name, columns_name_query_feed):
    rearranged_feed = ""
    for col_key in columns_name_query_feed.split(","):
        rearranged_feed += " {} = ? and".format(col_key)
    return "SELECT * FROM {} WHERE {}".format(table_name, drop_end_symbol(rearranged_feed, 3))


def queryfy_value(value):
    return f'{value}' if (isinstance(value, (int, float, complex, bool)) or value is None) else f"'{value}'"


def get_null_safe_select_query(table_name, df, select_query, data_row):

    key_map = get_column_datatype_map(table_name, df)
    new_data_row = []

    complete_query = select_query
    col_keys = key_map.keys()
    for cell_val, col_key in zip(data_row, col_keys):
        if cell_val is None:
            select_query = select_query.replace(
                f"{col_key} = ?", f"isnull({col_key}, 0) = 0")
            complete_query = complete_query.replace(
                f"{col_key} = ?", f"isnull({col_key}, 0) = 0")
        else:
            new_data_row.append(cell_val)

        col_val = queryfy_value(cell_val)
        complete_query = complete_query.replace(
            f"{col_key} = ?", f"{col_key} = {col_val}")

    # col_keys = [key for key in key_map]
    # for col_num in range(len(data_row)):
    #     if data_row[col_num] is None:
    #         select_query = select_query.replace("{} = ?".format(col_keys[col_num]),
    #                                             "isnull({}, 0) = 0".format(col_keys[col_num]))
    #     else:
    #         new_data_row.append(data_row[col_num])

    return select_query, new_data_row, complete_query
