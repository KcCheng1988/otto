import os
import logging
import logging.config
from logging import Logger

from config import CONF_DATA, CONF_LOGGER

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

def configure_logger(module : str = "temp") -> Logger :
    """ Return logger configuration dictionary.

    Params:
    -------
        * module (str) :    Name of the module within the preprocessing package. Default as temp
                            if unspecified.
    
    Return:
        * Logger :  A logger object
    """
    CONF_LOGGER["handlers"]["eda_fh"]["filename"] = os.path.join(LOG_DIR, f"{module}.log")
    logging.config.dictConfig(CONF_LOGGER)
    logger = logging.getLogger(f"{__name__}.{module}")

    return logger

