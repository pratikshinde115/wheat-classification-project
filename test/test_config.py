import json
import logging
import os
import joblib
import pytest
import prediction


input_data = {
    "incorrect_range": {
        "area": 7.897897,
        "perimeter": 5.55,
        "compactness": 0.199,
        "length_of_kernel": 1.99,
        "width_of_kernel": 1.2,
        "asymmetry_coefficient": 0.6789,
        "length_of_kernel_groove": 1.75,
    },
    "correct_range": {
        "area": 17.897897,
        "perimeter": 15.55,
        "compactness": 0.899,
        "length_of_kernel": 5.99,
        "width_of_kernel": 3.2,
        "asymmetry_coefficient": 1.6789,
        "length_of_kernel_groove": 5.75,
    },
    "incorrect_col": {
        "area": 78.97897,
        "perimeter": 55.5,
        "compactness": 199,
        "length_of_kernel": 199,
        "width_of_kernel": 12,
        "asymmetry_coefficient": 67.89,
        "length_of_kernel_groove": 17.5,
    },
}

TARGET_range = {"v1": 1, "v2": 2, "v3": 3}


def test_form_response_correct_range(data=input_data["correct_range"]):
    res = prediction.form_response(data)
    assert TARGET_range["v1"] or TARGET_range["v2"] or TARGET_range["v3"]


def test_api_response_correct_range(data=input_data["correct_range"]):
    res = prediction.api_response(data)
    assert (
        TARGET_range["v1"] == res["response"]
        or TARGET_range["v2"] == res["response"]
        or TARGET_range["v3"] == res["response"]
    )


def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction.NotInRange):
        res = prediction.form_response(data)


def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = prediction.api_response(data)
    assert res["response"] == prediction.NotInRange().message


def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = prediction.api_response(data)
    assert res["response"] == prediction.NotInCols().message