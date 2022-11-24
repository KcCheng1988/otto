'''
https://nurdabolatov.com/parallel-processing-large-file-in-python
'''
import multiprocessing as mp
import pandas as pd
import json

from otto.preprocessing.tab import single_session
from . import CONF_DATA

def write_to_csv(src_fname : str, dest_fname : str) -> None:
    """
    """
    with open(dest_fname, 'w') as dest_csv:
        dest_csv.write("session,aid,ts,type")
        with open(src_fname, 'r') as src_f:
            for ln in src_f:
                session = json.loads(ln)
                ss, events = session["session"], session["events"]
                for event in events:
                    dest_csv.write("\n{},{},{},{}".format(ss, event["aid"], event["ts"], event["type"]))           
    

if __name__ == "__main__":
    src_fname = CONF_DATA["train"]["raw"]
    write_to_csv(src_fname, CONF_DATA["train"]["raw_csv"])

