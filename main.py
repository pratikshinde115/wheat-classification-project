from logger import logging
import argparse
from pipeline import get_and_load_data, processing_data, split_data, train_and_evaluate


def pipeline(config_path):
    """_summary_

    Args:
        config_path (_type_): _description_
    """
    try:
        logging.info("Step1: Running the process of get_and_load_data")
        get_and_load_data.get_data(config_path)
        logging.info("Step2: Running the processing_data step")
        processing_data.processing_df(config_path)
        logging.info("Step3: Running the split_and_saved_data")
        split_data.split_and_saved_data(config_path)
        logging.info("Step4:inally train_and_evaluate Step is started")
        train_and_evaluate.train_and_evaluate(config_path)
        logging.info("----------------Pipeline is completed!----------------")
        logging.info("")
    except Exception as e:
        logging.warning(f"Pipeline is not start and the reason is: {e}")
        print(e)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="config.yaml")
    parsed_args = args.parse_args()
    logging.info("----------------Starting the Pipeline----------------")
    pipeline(config_path=parsed_args.config)
