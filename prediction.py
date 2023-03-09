import json
import pickle as pkl
import numpy as np
import argparse
from pipeline.get_and_load_data import read_params
import yaml
import pandas as pd
from logger import logging




args = argparse.ArgumentParser()
args.add_argument("--config", default="config.yaml")
parsed_args = args.parse_args()
config = read_params(parsed_args.config)


def read_params(config_path) -> str:
    """
    help to read the params that are present inside the config.yaml file
    """
    try:
        with open(config_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    except Exception as e:
        logging.warning(f"Error in reading config.yaml file is: {e}")
        print(e)


schema_path = config["SCHEMA_PATH"]
model_path = config["MODEL_PATH"]
transform_path = config["TRANSFORMER_PATH"]


class NotInRange(Exception):
    def _init_(self, message="Values entered are not in expected range"):
        self.message = message
        super()._init_(self.message)


class NotInCols(Exception):
    def _init_(self, message="Not in cols"):
        self.message = message
        super()._init_(self.message)


def get_category(pred_result):
    """help to get the category name from the classified output from the model
    Args:
        pred_result (int): ordinal value

    Returns:
        response (str): name of the category
    """
    try:
        pred_result = int(pred_result)
        if pred_result == 0:
            response = "Kama"
        elif pred_result == 1:
            response = "Rosa"
        else:
            response = "Canadian"
        logging.info(f"get category is Done and the category is:{response}")
        return response
    except Exception as e:
        logging.warning(f"Error occur in get category is {e}")
        print(e)


def predict(data):
    """predict the df using model and transform

    Args:
        data (DataFrame): user enter value in form of df

    Returns:
        prediction (int): ordinal value range from 0-2
    """
    try:
        transformer = pkl.load(open(transform_path, "rb"))
        model = pkl.load(open(model_path, "rb"))
        transform_data = pd.DataFrame(transformer.transform(data), columns=data.columns)
        prediction = model.predict(transform_data).tolist()[0]
        logging.info(f"Prediction is done and the predicted value is:{prediction}")
        return prediction
    except Exception as e:
        logging.warning(f"Error in predict is {e}")
        print(e)


def get_schema(schema_path=schema_path):
    """get the schema from the yaml file name config

    Args:
        schema_path (str): location of the config.yaml file

    Returns:
        schema (dict): schema of df which contains min and max values
    """
    try:
        with open(schema_path) as json_file:
            schema = json.load(json_file)
            logging.info("get schema is done!")
        return schema
    except Exception as e:
        logging.warning(f"Error in get schema is : {e}")
        print(e)


def validate_input(dict_request):
    """it check the input provides by the user is correct or not

    Args:
        dict_request (dict): request.form from website constains user input data in the from of dict
    Raises:
        NotInCols: Error
        NotInRange: Error

    Returns:
        (boolean): to check its True or False
    """

    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        if not (
            schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]
        ):
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)
    logging.info("validating input is Done!")
    return True



def form_response(dict_request):
    """help to called the validate input fuction and convert the users input into df

    Args:
        dict_requlogging.warning(f"Error in website is: {e}")est (dict): form data in form of dict

    Returns:
        repsonse : Final out on the webpage/website
    """
    try:
        if validate_input(dict_request):
            data = (pd.DataFrame.from_dict(dict_request, orient="index")).T
            pred_result = predict(data)
            response = get_category(pred_result)
            logging.info("get category is Done")
            return response
    except Exception as e:
        logging.warning(f"Error in form response is: {e}")
        print(e)


def api_response(dict_request):
    """ "api response helps to get the output if its in the from of json

    Args:
        dict_request (json): dict_request is in the form of json

    Returns:
        response: output on the website/wepage
    """
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response": response}
            logging.info(f"api response is completed and response is {response}")
            return response

    except NotInRange as e:
        response = {"the_exected_range": get_schema(), "response": str(e)}
        return response

    except NotInCols as e:
        response = {"the_exected_cols": get_schema().keys(), "response": str(e)}
        return response

    except Exception as e:
        response = {"response": str(e)}
        logging.warning(f"Error in api_response is: {e}")
        return response