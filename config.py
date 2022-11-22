from pathlib import Path

###################################################
# Project directories here
###################################################
PROJ_DIR = Path(__file__).parent.absolute()
CONF_DIR = PROJ_DIR / "conf" / "local"  # Update the yaml files in your own local configuration directory.
DATA_DIR = PROJ_DIR / "data"
SRC_DIR = PROJ_DIR / "otto"
TEST_DIR = PROJ_DIR / "test"