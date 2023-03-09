from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import pandas as pd
import prediction
from logger import logging


webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(_name_, static_folder=static_dir, template_folder=template_dir)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        try:
            if request.form:
                dict_req = dict(request.form)
                response = prediction.form_response(dict_req)
                logging.info("Adding response in main page throught dict")
                return render_template("main.html", response=response)
            elif request.json:
                print(request.json)
                response = prediction.predict(
                    (pd.DataFrame.from_dict(request.json, orient="index")).T
                )
                logging.info("Adding response in main page throught json")
                return jsonify(response)

        except Exception as e:
            logging.warning(f"Error in website is: {e}")
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            error = {"error": e}
            logging.info("Calling 404 page")
            return render_template("404.html", error=error)
    else:
        logging.info("Render the main page of website")
        return render_template("main.html")


if _name_ == "_main_":
    app.run(debug=True)