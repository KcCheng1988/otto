from pathlib import Path
from otto.utils.io import load_yaml

###################################################
# Project directories here
###################################################
PROJ_DIR = Path(__file__).parent.absolute()
CONF_DIR = PROJ_DIR / "conf" / "local"  # Update the yaml files in your own local configuration directory.
DATA_DIR = PROJ_DIR / "data"
SRC_DIR = PROJ_DIR / "otto"
TEST_DIR = PROJ_DIR / "test"

CONF_DATA = load_yaml(CONF_DIR / "data.yaml")
CONF_LOGGER = load_yaml(CONF_DIR / "logging.yaml")