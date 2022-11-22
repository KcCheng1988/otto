import os
import logging
import logging.config
from logging import Logger
from typing import Dict
from config import CONF_DIR
from otto.utils.io import load_yaml

# Load the configuration dictionaries
CONF_DATA = load_yaml(CONF_DIR / "data.yaml")
# CONF_LOGGER = load_yaml(CONF_DIR / "logging.yaml")

# Set the log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

def configure_logger(module : str = "temp") -> Logger :
    """ Return logger configuration dictionary.

    Params:
    -------
        * module (str) :    Name of the module within the preprocessing package. Default as temp
                            if unspecified.
    
    Return:
        * Logger :  A logger object
    """
    CONF_LOGGER = load_yaml(CONF_DIR / "logging.yaml")
    CONF_LOGGER["handlers"]["preprocessing_fh"]["filename"] = os.path.join(LOG_DIR, f"{module}.log")

    logging.config.dictConfig(CONF_LOGGER)
    logger = logging.getLogger(f"{__name__}.{module}")

    return logger
