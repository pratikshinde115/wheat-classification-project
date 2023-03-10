import pytest
import yaml
import os
import json
import argparse
from pipeline.get_and_load_data import read_params


args = argparse.ArgumentParser()
args.add_argument("--config", default="config.yaml")
parsed_args = args.parse_args()
config = read_params(parsed_args.config)
schema_path = config["SCHEMA_PATH"]


@pytest.fixture
def config(config_path="config.yaml"):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


@pytest.fixture
def schema_in(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema
