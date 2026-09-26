# data_loaders.py
from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(filepath)
    logging.info(f"Loaded CSV File: {filepath} ({len(df)} rows)")
    return df

def load_json(filepath):
    """Load a JSON file into a Python object (dict or list)."""
    file_dct = json.load(filepath)
    logging.info(f"Loaded a JSON File: {filepath}")
    return file_dct

def load_yaml(filepath):
    """Load a YAML file into a Python object."""
    file_yaml = yaml.safe_load(filepath)
    logging.info(f"Loaded a YAML File: {filepath}")
    return file_yaml

def load_data(filepath):
    """Load a file based on its extension."""
    path = Path(filepath)
    if path.suffix == ".csv":
        return load_csv(path)
    elif path.suffix == ".json":
        return load_json(path)
    elif path.suffix in (".yaml", "yml"):
        return load_yaml(path)
    else:
        logging.error(f"Unsupported file format: {path.suffix}")
        raise ValueError

