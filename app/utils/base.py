import json
import os.path
from pathlib import Path


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_config_path():
    return os.path.join(get_project_root(), "config.json")


def get_access_token():
    with open(get_config_path()) as json_file:
        config = json.load(json_file)
    return config['access_token']
