# PyDataImport

A Python package for importing data from various sources to SQL Server databases.

## Installation

You can install the package using pip:

```bash
pip install pydataimport
```

## Usage

```python
import pydataimport as pdi

# Import data from JSON
pdi.import_data(
    "json",
    data_source,
    "table_name",
    operation_mode=pdi.OPERATION_MODE['SINGLE_INSERT']
)

# Fetch data from database
data = pdi.fetch_data("SELECT * FROM your_table")

# Get current date in string format
current_date = pdi.date_str_now()

# Track script runtime
with pdi.track_script_runtime() as timer:
    # Your code here
    pass
```

## Features

- Data import from various sources (JSON, CSV, etc.)
- Database operations (fetch, execute stored procedures)
- Utility functions for date handling
- Script runtime tracking
- Environment configuration management

## Configuration

The package uses environment variables for configuration. Create a `.env` file with the following variables:

```env
# API Configuration
DATA_SRC_API_ENDPOINT=your_api_endpoint
DATA_SRC_TOKEN=your_api_token

# Database Configuration
DATA_DES_CONNECTION_TYPE=window  # or 'remote' for SQL authentication
DATA_DES_SERVER=your_server
DATA_DES_DB_NAME=your_database
DATA_DES_PORT=1433
DATA_DES_USERNAME=your_username
DATA_DES_PASSWORD=your_password
DATA_DES_DRIVER=SQL Server Native Client 11.0  # or your preferred SQL Server driver
DATA_DES_TABLE=your_table
DATA_DES_STORED_PROCEDURE=your_stored_procedure

# Operation Mode
OPERATION_MODE=DROP_OLD_CREATE_NEW
```

### SQL Server Driver Configuration

The package uses pyodbc to connect to SQL Server. You need to specify the correct driver name in the `DATA_DES_DRIVER` environment variable. Common driver names include:

- `SQL Server Native Client 11.0`
- `ODBC Driver 17 for SQL Server`
- `ODBC Driver 18 for SQL Server`

To find available drivers on your system, you can run:
```python
import pyodbc
print(pyodbc.drivers())
```

## Requirements

- Python 3.8 or higher
- SQL Server database
- Required Python packages (automatically installed with pip):
  - pandas
  - pyodbc
  - requests
  - python-dateutil
  - numpy

## License

This project is licensed under the MIT License - see the LICENSE file for details. 