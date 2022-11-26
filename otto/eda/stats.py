import pandas as pd
import numpy as np
from typing import Optional

from . import CONF_DATA, configure_logger

logger = configure_logger("stats")

def get_info(df : pd.DataFrame, name : Optional[str] = None) -> None:
    """ Print basic statistics of the input dataframe:
        * Row counts
        * Columns' name and types
        * Count of unique values in columns
        * Presence and count of nan or null values
    
    Params:
    -------
        * df (pd.DataFrame) : Input Pandas dataframe
        * name (str) : Name of the dataframe
    
    """
    info_dict = {}

    logger.info("({}) Top few rows:".format(name))
    logger.info('\n' + '='*40 + '\n' + str(df.head(6)) + '\n' + '='*40)
    info_dict["head"] = df.head(6)

    row_count = len(df)
    logger.info("Total number of rows: {}".format(row_count))
    info_dict["n_rows"] = len(df)

    rows = []
    for col in df.columns:
        df_col = df.loc[:, [col]]
        col_type = df_col[col].dtype
        unique_count = len(np.unique(df_col.values))
        n_na = int(df_col.isna().sum(axis=0))
        n_null = int(df_col.isnull().sum(axis=0))
        rows.append((col, col_type, unique_count, n_na, n_null))
    
    info_df = pd.DataFrame(rows, columns=["name", "type", "n_values", "n_na", "n_null"]).set_index("name")
    logger.info("Column information:")
    logger.info("\n" + '='*40 + '\n' + str(info_df) + '\n' + '='*40)
    info_dict["columns_info"] = info_df

    return info_dict

if __name__ == "__main__":
    fpath = CONF_DATA["test"]["raw_csv"]
    logger.info("Loading %s into Pandas dataframe.", fpath)
    df = pd.read_csv(fpath)
    logger.debug("Dataframe loaded successfully.")
    info_dict = get_info(df,"test")