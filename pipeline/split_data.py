import pandas as pd
from sklearn.model_selection import train_test_split
from pipeline.get_and_load_data import read_params
from logger import logging


def split_and_saved_data(config_path):
    """split the processed df into train and test, and also saving it into data/split folder too

    Args:
        config_path (str): has the path of config.yaml file
    """
    try:
        logging.info("3.1 Get config for splitting the df")
        config = read_params(config_path)
        test_data_path = config["SPLIT_DATA"]["TEST_CSV_PATH"]
        train_data_path = config["SPLIT_DATA"]["TRAIN_CSV_PATH"]
        process_data_path = config["PROCESSED_DATA"]["PROCESSED_CSV_PATH"]
        split_ratio = config["SPLIT_DATA"]["TEST_SIZE"]
        random_state = config["SPLIT_DATA"]["RANDOM_STATE"]
        stratify = [config["ESTIMATOR"]["TARGET_COL"]]
        df = pd.read_csv(process_data_path, sep=",")
        logging.info("3.2 Splitting is started")
        train, test = train_test_split(
            df, test_size=split_ratio, random_state=random_state, stratify=df[stratify]
        )
        train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
        logging.info("3.3 Train csv is generated")
        test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")
        logging.info("3.4 Test csv is also generated")
        logging.info("3.5 Splitting is Completed!")
    except Exception as e:
        logging.warning(f"Error occur while splitting is: {e}")
        print(e)
