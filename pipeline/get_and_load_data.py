import yaml
import pandas as pd
from logger import logging


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


def saving(df, config_path) -> None:
    """Loading the new converted Dataframe and save it to inside data/raw folder

    Args:
        df (DataFrame): newly converted df from .txt
        config_path (str): path of the yaml file that contains the configurations
    """
    try:
        config = read_params(config_path)
        raw_data_path = config["LOAD_DATA"]["RAW_CSV_PATH"]
        df.to_csv(raw_data_path, sep=",", index=False, encoding="utf-8")
        logging.info("1.5 Saving into data/raw folder is done!")
    except Exception as e:
        logging.warning(f"Error occur in saving the df, error is:{e}")
        print(e)


def convert_to_df(data_path):
    """conveting the txt file into df
    Args:
        data_path (file): text file contain the data.

    Returns:
        df (DataFrame): converted df from txt file.
    """
    try:
        columns_names = [
            "area",
            "perimeter",
            "compactness",
            "length_of_kernel",
            "width_of_kernel",
            "asymmetry_coefficient",
            "length_of_kernel_groove",
            "Target",
        ]

        df = pd.read_csv(
            data_path, delimiter="\t", encoding="utf-8", names=columns_names
        )
        logging.info("1.3 completion of converting into df is successfull!")
        return df
    except Exception as e:
        logging.warning(f"error occur is converting data into df, the error is {e}")
        print(e)


def get_data(config_path) -> None:
    """is the functin that call the other function such as convert_df, saving for getting data and saving it into df
    Args:
        config_path (str): path of yaml file which contains the configurations
    """
    try:
        logging.info("1.1 Read the config_path to get the given dataset path")
        config = read_params(config_path)
        data_path = config["DATA_SOURCE"]["EXTRACT_DATA"]
        logging.info("1.2 Converting of given dataset into to Dataframe is started")
        convert_df = convert_to_df(data_path)
        logging.info("1.4 saving of converted df is started")
        saving(convert_df, config_path)
        logging.info("1.6 get and load data into df is Fully Completed!")
    except Exception as e:
        logging.warning(f"Error occuring in getting data is : {e}")
        print(e)
