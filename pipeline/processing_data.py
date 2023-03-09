from sklearn.preprocessing import StandardScaler
import pickle as pkl
import pandas as pd
from pipeline.get_and_load_data import read_params
from logger import logging


def scaler_transformer(df):
    """Helps to convert the df into scaled df using standard scaler

    Args:
        df (DataFrame): raw dataframe from data/raw/raw_wheat.csv

    Returns:
        scaled_df, scaler_obj
    """
    try:
        scaler_obj = StandardScaler()
        target = df[["Target"]]
        df.drop(columns=["Target"], inplace=True)
        scaled_df = pd.DataFrame(scaler_obj.fit_transform(df), columns=df.columns)
        scaled_df["Target"] = target
        logging.info("2.3 Transforming of df is completed!")
        return scaled_df, scaler_obj
    except Exception as e:
        logging.warning(f"Error occur during transformation is : {e}")
        print(e)


def processing_df(config_path) -> None:
    """contains other funciton which helps to convert raw df into processed df and saving it

    Args:
        config_path (str): path of yaml file which has configuration for project
    """
    try:
        logging.info("2.1 Read the config for processing the df")
        config = read_params(config_path)
        raw_data_path = config["LOAD_DATA"]["RAW_CSV_PATH"]
        process_data_path = config["PROCESSED_DATA"]["PROCESSED_CSV_PATH"]
        schema_path = config["SCHEMA_PATH"]
        transformer_path = config["TRANSFORMER_PATH"]
        df = pd.read_csv(raw_data_path, sep=",")
        schema_df = (
            df.drop(columns=["Target"])
            .describe()
            .loc[["min", "max"]]
            .to_json(schema_path)
        )
        logging.info("2.2 Transforming the df using standard scaler and saving it")
        processed_df, scaler_obj = scaler_transformer(df)
        processed_df.to_csv(process_data_path, sep=",", index=False, encoding="utf-8")
        logging.info("2.4 Saving transformed df Done!")
        pkl.dump(scaler_obj, open(transformer_path, "wb"))
        logging.info("2.5 Saving scaler tranformer object is also Done!")
        logging.info("2.6 Processing of df is Completed!!")
    except Exception as e:
        logging.warning(f"Error occur in processing the df is : {e}")
        print(e)
