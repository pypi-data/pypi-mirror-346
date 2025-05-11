from pydataimport.services.db.datatype_service import get_column_datatype_map
from pydataimport.utils.common_util import is_missing_value, drop_end_symbol
import pandas as pd


def process_data(table_name, df):
    
    key_map = get_column_datatype_map(table_name, df)
    if key_map is None:
        return None

    columns_to_sustain = [key_map[key]["column_name"] for key in key_map]
    df = df[columns_to_sustain]

    for col_key in key_map:

        col_name = key_map[col_key]["column_name"]
        col_db_datatype = key_map[col_key]["db_datatype"]
        db_dtype_split = col_db_datatype.split("(")
        col_db_datatype_initial = db_dtype_split[0]

        # round off the decimal values
        if col_db_datatype_initial == "decimal":
            decimal_split = db_dtype_split[1].split(",")
            decimal_len = int(decimal_split[0])
            decimal_round = int(drop_end_symbol(decimal_split[1]))

            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            df[col_name] = df[col_name].replace(0, 0.0)
            df[col_name] = df[col_name].astype(float).round(decimal_round)
            # df.loc[:, col_name] = df.loc[:, col_name].round(decimal_round)

    # return [[None if is_missing_value(y) else y for y in x] for x in df.values]
    return df.apply(lambda x: [None if pd.isnull(y) else y for y in x], axis=1).values.tolist()

