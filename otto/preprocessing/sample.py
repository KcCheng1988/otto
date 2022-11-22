import json, os
from typing import List, Dict

from . import CONF_DATA
from . import configure_logger

# Configure logger
logger = configure_logger("sample")

def view_raw(n_lines : int =10, mode : str = "train") -> List[Dict]:
    """ Returns the first few lines of the raw dataset stored in .jsonl format.

    Params:
    -------
        * n_lines (str) : Number of lines in the files to be returned.
        * mode (str) : Type of dataset. 
            * "train" for train data. Default value.
            * "test" for test data

    Returns:
    -------
        * List[Dict] : A list of data, each datum as dictionary object.

    """
    if mode == "train":
        fpath = CONF_DATA["train"]["raw"]
    elif mode == "test":
        fpath = CONF_DATA["test"]["raw"]
    logger.debug("%s data located at %s", mode.capitalize(), fpath)

    
    i = 0
    rows = []
    with open(fpath, 'r') as f:
        while i < n_lines:
            json_ln = f.readline()

            # Each line of the file is a json-like dictionary
            data = json.loads(json_ln)
            rows.append(data)

            i+=1
    logger.debug("Successfully reading %d lines of %s data: \n %s", n_lines, mode, rows)

    return rows

if __name__ == "__main__":
    sample = view_raw(3, "train")