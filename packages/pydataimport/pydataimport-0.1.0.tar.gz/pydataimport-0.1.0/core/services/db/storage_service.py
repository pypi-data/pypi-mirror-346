
import logging
import pyodbc


def get_local_db_conn(driver, server, db_name):
    return pyodbc.connect("Driver={"+driver+'}'+f";Server={server};Database={db_name};Trusted_Connection=yes;")


def get_remote_sql_server_conn(driver, server_ip, server_port, database_name, database_username, database_password):
    CONN_URL = "Driver={"+driver+'};' + \
        f"SERVER={server_ip};DATABASE={database_name};UID={database_username};" + \
        'PWD={'+database_password+'};'
    # print(f'conn_url: {CONN_URL}')
    return pyodbc.connect(CONN_URL)


def get_sql_server_connection(connection_type, server, port, database_name, username, password):

    # SQL Server Database Connection
    drivers = [item for item in pyodbc.drivers()]
    driver = drivers[2]
    # driver = get_db_driver()
    
    # SQL Server Database Connection
    if connection_type == "window":
        return get_local_db_conn(driver, server, database_name)
    elif connection_type == "remote":
        return get_remote_sql_server_conn(driver, server, port, database_name, username, password)
    else:
        logging.error("Database Connection Type Error")
        return None


def get_sqlserver_py_datatype_map():
    return {
        "varchar": "str",
        "int": "int",
        "smallint": "int",
        "bigint": "float",
        "decimal": "float",
        "datetime2": "datetime",
        "text": "str",
        "datetime": "datetime",
        "smalldatetime": "datetime",
        "bit": "bool"
    }


def get_db_datatypes_list():
    return ["varchar(124)", "int", "bigint", "smallint", "decimal(10,2)", "datetime2"]

