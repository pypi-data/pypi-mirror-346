import traceback
import logging
import pydataimport.services.db.storage_service as ss
import contextlib
from pydataimport.config.env_config import env_object
# SQL Server Database Connection
connection_type = env_object.DATA_DES_CONNECTION_TYPE
server = env_object.DATA_DES_SERVER
db_name = env_object.DATA_DES_DB_NAME
port = env_object.DATA_DES_PORT
username = env_object.DATA_DES_USERNAME
password = env_object.DATA_DES_PASSWORD


@contextlib.contextmanager
def db_con():
    global connection_type, server, db_name, port, username, password
    conn = None
    # Insert data into database
    try:
        conn = ss.get_sql_server_connection(connection_type, server, port, db_name, username, password)
        yield conn 
    except Exception as e:
        # activity_log["main"] = str(e)
        logging.error(f"Database Connection Error: {e}")
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
    # logging.error("Data Error")
