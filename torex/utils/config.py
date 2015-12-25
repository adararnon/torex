"""Configuration utils"""
import yaml


def read_config(config_path):
    """
    Reads the configuration from a file.
    :param config_path: The configuration file's path
    :return: The parsed configuration dict
    """
    with open(config_path, 'r') as configf:
        return yaml.load(configf)
