"""Global configuration handling."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

#TODO consider moving nb_info to _config.yml

DEFAULT_CONFIG = {
    "nbs": os.path.join(os.path.dirname(__file__), '../../notebooks/*.ipynb'),
    "nb_read_path": os.path.join(os.path.dirname(__file__), '../../notebooks/'),
    "nb_write_path": os.path.join(os.path.dirname(__file__), '../../docs/_notebooks/'),
    "asset_write_path": os.path.join(os.path.dirname(__file__), '../../docs/assets/'),
    "asset_subdirs": ['figures', 'data', 'images', 'imgs', 'img'],
    "nb_nav_top": True,
    "nb_nav_bottom": True,
}


def get_config():
    """Retrieve the config from the specified path, returning a config dict."""
    #TODO
    config_dict = DEFAULT_CONFIG
    return config_dict

def get_user_config(config_file=None, default_config=False):
    """Return the user config as a dict"""
    #TODO
    pass