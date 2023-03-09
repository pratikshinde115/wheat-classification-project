from logger import logging
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix
from pipeline.get_and_load_data import read_params
import pickle as pkl
import json


def eval_metrics(actual, pred):
    """evaluating the model using various metrics

    Args:
        actual (np.arrary): actual values i.e test_y
        pred (np.array): predicted values by model on test_y

    Returns:
        f1, recall, precision, cnf_matrix
    """
    try:
        f1 = f1_score(actual, pred, average="micro")
        recall = recall_score(actual, pred, average="micro")
        precision = precision_score(actual, pred, average="micro")
        cnf_matrix = confusion_matrix(actual, pred)
        logging.info("4.5 evaluation of metrics is completed!")
        return f1, recall, precision, cnf_matrix

    except Exception as e:
        logging.warning(f"Error occur during metrics evaluation is: {e}")
        print(e)


def train_and_evaluate(config_path):
    """Provide the training and testing of the model and saving it into  params.json, scores.json and model.pkl
    Args:
        config_path (str): path of config.yaml file
    """
    try:
        logging.info("4.1 Read the config for train and evaluating")
        config = read_params(config_path)
        test_data_path = config["SPLIT_DATA"]["TEST_CSV_PATH"]
        train_data_path = config["SPLIT_DATA"]["TRAIN_CSV_PATH"]
        random_state = config["SPLIT_DATA"]["RANDOM_STATE"]
        model_path = config["MODEL_PATH"]

        reg_param = config["ESTIMATOR"]["QUADRATIC_DISCRIMINANT_ANALYSIS"]["PARAMS"][
            "REG_PARAM"
        ]
        store_covariance = config["ESTIMATOR"]["QUADRATIC_DISCRIMINANT_ANALYSIS"][
            "PARAMS"
        ]["STORE_COVARIANCE"]
        tol = config["ESTIMATOR"]["QUADRATIC_DISCRIMINANT_ANALYSIS"]["PARAMS"]["TOL"]
        target = [config["ESTIMATOR"]["TARGET_COL"]]

        train = pd.read_csv(train_data_path, sep=",")
        test = pd.read_csv(test_data_path, sep=",")

        train_y = train[target]
        test_y = test[target]

        train_x = train.drop(target, axis=1)
        test_x = test.drop(target, axis=1)
        logging.info("4.2 clf-model variable is created for classification")
        clf = QuadraticDiscriminantAnalysis(
            reg_param=reg_param, store_covariance=store_covariance, tol=tol
        )
        clf.fit(train_x, train_y)
        logging.info("4.3 model training is completed!")

        predicted_qualities = clf.predict(test_x)
        actual = test_y["Target"].tolist()
        logging.info("4.4 Evalution of metrics is begin")
        f1, recall, precision, cnf_matrix = eval_metrics(actual, predicted_qualities)
        print(
            "QuadraticDiscriminantAnalysis model (reg_param=%f, store_covariance=%f, tol=%f):"
            % (reg_param, store_covariance, tol)
        )
        print("  F1 Score: %s" % f1)
        print("  Recall: %s" % recall)
        print("  Precision: %s" % precision)
        print("  Confusin Matrix: %s" % cnf_matrix)

        #####################################################
        scores_file = config["REPORTS"]["SCORES"]
        params_file = config["REPORTS"]["PARAMS"]

        with open(scores_file, "w") as f:
            scores = {"f1_score": f1, "recall": recall, "precision": precision}
            json.dump(scores, f, indent=4)
            logging.info("4.6 Saving the scores in json is completed")
        with open(params_file, "w") as f:
            params = {
                "reg_param": reg_param,
                "store_covariance": store_covariance,
                "tol": tol,
            }
            json.dump(params, f, indent=4)
            logging.info("4.7 also saving parameter into json is done too!")
        #####################################################

        pkl.dump(clf, open(model_path, "wb"))
        logging.info("4.8 Saving trained model into pickle file is completed")
        logging.info("4.9 training and evaluation of model is Completed!!")

    except Exception as e:
        logging.warning(f"Error occur while train and evaluating model is: {e}")
