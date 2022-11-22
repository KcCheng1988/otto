import yaml
from typing import Dict

def load_yaml(fpath : str) -> Dict :
    """ Load a yaml configuration file and return the configuration dictionary.

    Params:
    -------
        * fpath (str) : Path to the configuration yaml file.
    
    Returns:
    -------
        * Dict : Configuration dictionary object.

    """
    with open(fpath, 'r') as f:
        data = yaml.safe_load(f)
    
    return data

def save_yaml(config_dict : Dict, fpath: str) -> None:
    """ Dump a configuration dictionary to a yaml file.

    Params:
    -------
        * config_dict (Dict) : Configurationi dictionary object.
        * fpath (str) : Path to the output configuration yaml file.

    """
    with open(fpath, 'w') as f:
        yaml.dump(config_dict, f)