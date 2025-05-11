import pyodbc
import logging
from datetime import datetime
import pydataimport.config.db_config as db
from pydataimport.services.db.data_storage_query_service import create_new_table_query
from pydataimport.services.db.data_storage_query_service import create_insert_query
from pydataimport.services.db.data_storage_query_service import create_select_query
from pydataimport.services.db.data_storage_query_service import create_complete_insert_query
from pydataimport.services.db.data_storage_query_service import get_null_safe_select_query
from pydataimport.utils.common_util import is_percent_div_by, percent


def dump_all_data(conn, table_name, insert_query_feed, data):
    insert_query = create_insert_query(table_name, insert_query_feed)
    is_success = False
    cur = conn.cursor()
    logging.info(f"Inserting data into {table_name}")
    try:
        conn.autocommit = False
        cur.executemany(insert_query, data)  # df.values.tolist())
        conn.commit()
    except Exception as e:  # pyodbc.DatabaseError as e:
        conn.rollback()
        logging.error(f"Error in inserting data into {table_name}, Error:{e}")
        raise e
    else:
        conn.commit()
        is_success = True
    finally:
        conn.autocommit = True
    return is_success


def drop_table(conn, table_name):
    cur = conn.cursor()
    try:
        cur.execute("IF (OBJECT_ID('{}') IS NOT NULL ) BEGIN DROP TABLE {} END".format(
            table_name, table_name))
    except pyodbc.DatabaseError as e:
        raise e
    else:
        conn.commit()
        logging.info(f"Table {table_name} dropped successfully")
        return True


def create_table(conn, table_name, create_table_query_feed):
    create_table_query = create_new_table_query(
        table_name, create_table_query_feed)
    cur = conn.cursor()
    # cur.execute(f"USE {db_name}")
    try:
        cur.execute(create_table_query)
    except pyodbc.DatabaseError as e:
        cur.rollback()
        raise e
    else:
        cur.commit()
        logging.info(f"Table {table_name} created successfully")
        return True


def safe_dump_data(conn, table_name, df, insert_query_feed, data_rows):
    logging.info(f"Inserting data into {table_name} in safe mode")
    insert_query = create_insert_query(table_name, insert_query_feed)
    select_query = create_select_query(table_name, insert_query_feed)

    cur = conn.cursor()
    row_num = 0
    failed_rows = []
    try:
        # conn.autocommit = False
        for data_row in data_rows:
            cur_data_row = data_row
            row_select_query, select_data_row, complete_select_query = get_null_safe_select_query(
                table_name, df, select_query, data_row)

            # df.values.tolist())
            cur.execute(row_select_query, select_data_row)
            # print(select_query)
            # print(row_num, data_row)
            fetched_row = cur.fetchone()
            if fetched_row is None:
                cur.execute(insert_query, data_row)  # df.values.tolist())
            else:
                failed_rows.append(
                    {"row_num": row_num, "error": "Duplicate Record"})
            row_num += 1
            if row_num % 100 == 0:
                conn.commit()
                logging.info(f"Inserted(Committed) {row_num} rows")

        # conn.commit()
    except pyodbc.DatabaseError as e:
        conn.rollback()
        complete_insert_query = create_complete_insert_query(
            table_name, insert_query_feed, cur_data_row, 'NULL')
        failed_rows.append({"row_num": row_num, "error": repr(e)})
        logging.error(
            f"Failed to insert data at row {row_num+1} \nError:{e}\nSQ:{complete_select_query}\nIQ:{complete_insert_query}")
        # print("Failed to insert data at row {}".format(row_num))
        raise e
    else:
        conn.commit()
    finally:
        cur.close()

    return failed_rows
    # conn.autocommit = True


def dump_data(conn, table_name, df, insert_query_feed, data_rows):
    logging.info(f"Inserting data into {table_name} in individual mode")
    insert_query = create_insert_query(table_name, insert_query_feed)

    cur = conn.cursor()
    row_num = 0
    failed_rows = []
    try:
        # conn.autocommit = False
        # # temp code
        # row_num = 24800
        # data_rows = data_rows[row_num:]

        for data_row in data_rows:
            cur_data_row = data_row

            try:
                cur.execute(insert_query, data_row)  # df.values.tolist())
            except Exception as e:
                # generates Insert query for the failed row
                complete_insert_query = create_complete_insert_query(table_name, insert_query_feed, cur_data_row, 'NULL')
                failed_rows.append({"row_num": row_num, "error": repr(e)})
                logging.error(f"Failed to insert data at row {row_num+1} \nError:{e}\nIQ:{complete_insert_query}")

            row_num += 1
            if is_percent_div_by(10, row_num, len(data_rows)): #row_num % 1000 == 0:
                conn.commit()
                logging.info(f"Inserted(Committed) {row_num} rows")
                print(f'Row {row_num} - Completed {percent(row_num, len(data_rows))} %')

        # conn.commit()
    except Exception as e:  # pyodbc.DatabaseError as e:
        conn.rollback()
        # generates Insert query for the failed row
        complete_insert_query = create_complete_insert_query(
            table_name, insert_query_feed, cur_data_row, 'NULL')

        failed_rows.append({"row_num": row_num, "error": repr(e)})

        logging.error(f"Failed to insert data at row {row_num+1} \nError:{e}\nIQ:{complete_insert_query}")
        # print("Failed to insert data at row {}".format(row_num))
        raise e
    else:
        conn.commit()
    finally:
        cur.close()

    return failed_rows
    # conn.autocommit = True


def delete_all_old_data(conn, table_name):
    # time stamp
    # now = datetime.datetime.now() - datetime.timedelta(minutes=30)
    # created_at_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    cur = conn.cursor()
    try:
        cur.execute(
            f"DELETE FROM {table_name} WHERE created_at < (SELECT MAX(created_at) FROM {table_name})")
        # cur.execute("DELETE FROM {} WHERE created_at < '{}'".format(
        #     table_name, created_at_timestamp))
    except pyodbc.DatabaseError as e:
        logging.error(
            f"Failed to delete old data from table {table_name} : {e}")
        raise e
    else:
        conn.commit()
        logging.info(f"All old data deleted successfully")
        return True


def fetch_data(query, params=None, fetch=True, do_commit=False):
    try:
        with db.db_con() as conn:
            # Create a cursor object
            cursor = conn.cursor()
            # Execute the query
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            if not fetch:
                rows = None
            else:
                # Fetch all the rows
                rows = cursor.fetchall()

            if do_commit:
                conn.commit()
                
            # Close the cursor and connection
            cursor.close()

            return rows
    except Exception as e:
        logging.error(f"Error in fetching data from database: {e}")
        return None
    