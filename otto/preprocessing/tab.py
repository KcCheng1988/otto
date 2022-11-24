''' 
The objective of this script is to tabularize the events data per session into rows of events.

As an example, we have the following events in a session, captured as a JSON-like dictionary:
{'session': 12899780, 'events': [{'aid': 1142000, 'ts': 1661724000378, 'type': 'clicks'},  {'aid': 582732, 'ts': 1661724058352, 'type': 'clicks'}]}
We want to transform the dictionary into a table as follows, do the same for all sessions, and combine them together.
-------------------------------------------------
| session  |   aid   |       ts      |   type   |
-------------------------------------------------
| 12899780 | 1142000 | 1661724000378 | 'clicks' |
-------------------------------------------------
| 12899780 | 582732  | 1661724058352 | 'clicks' |
-------------------------------------------------

'''

from typing import Dict, List, Tuple
import pandas as pd

from otto.preprocessing.sample import view_raw


# Configure logger
from . import configure_logger
logger = configure_logger("tab")

def single_session(ss_dict : Dict) -> List[Tuple]:
    """ Transforms the events data of a single session in JSON-like dictionary
    into a list of tuples with four elements, representing (session, aid, ts, type).

    Params:
    -------
        * ss_dict (Dict) : Events data of a single session
    
    Returns:
    -------
        * List[Tuple] : A list of tuples (session, aid, ts, type), each element 
                        representing a single event in a session.
    
    """
    ss, events = ss_dict["session"], ss_dict["events"]

    rows = [(ss, event["aid"], event["ts"], event["type"]) for event in events]

    return rows

def multiple_session(ss_list : List[Dict]) -> List[Tuple]:
    """ Transforms the events data of all sessions into a list of tuples representing
    (session, aid, ts, type).

    Params:
    -------
        * ss_list (List[Dict]) : List of session with events data in JSON-like dictionary
    
    Returns:
    -------
        * List[Tuple] : A list of tuples (session, aid, ts, type).
    """
    rows = [row for ss in ss_list for row in single_session(ss)]

    logger.debug("Successfully tabularize sample dataset:")
    for row in rows:
        logger.debug(row)

    return rows

def to_csv(ss_list : List[Dict], dest_f : str) -> None:
    """ Transforms the events data of all sessions into a table of columns 
    (session, aid, ts, type) and output the result as csv.

    Params:
    -------
        * ss_list (List[Dict]) : List of session with events data in JSON-like dictionary
        * dest_f (str) : Path of the output csv
    
    Returns:
    -------
        * A csv file of four columns (session, aid, ts, type)
    
    """
    rows = multiple_session(ss_list)

    header = ["session", "aid", "ts", "type"]
    pd.DataFrame(rows).to_csv(dest_f, index=False, header=header)
    logger.info("Saving to %s successful.", dest_f)


if __name__ == "__main__":
    from . import CONF_DATA

    test_sample = view_raw(100, "test")
    to_csv(test_sample, CONF_DATA["test"]["sample"]["csv"])    

    train_sample = view_raw(100, "train")
    to_csv(train_sample, CONF_DATA["train"]["sample"]["csv"])
