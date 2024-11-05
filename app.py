# importing necessary libraries:
from flask import Flask, render_template, request
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

# creating the flask app:
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET","POST"])
def result():
    if request.method=="POST":

        carat = request.form["carat"]
        cut = request.form["cut"]
        color = request.form["color"]
        clarity = request.form["clarity"]
        depth = request.form["depth"]
        table = request.form["table"]
        x = request.form["x"]
        y = request.form["y"]
        z = request.form["z"]

        prediction_data_dict = {
            "carat" : [float(carat)],
            "cut" : [str(cut)],
            "color" : [str(color)],
            "clarity" : [str(clarity)],
            "depth" : [float(depth)],
            "table" : [float(table)],
            "x" : [float(x)],
            "y" : [float(y)],
            "z" : [float(z)]
        }

        prediction_data = pd.DataFrame(prediction_data_dict)

    return render_template("result.html")


if __name__=="__main__":
    app.run(debug=True)
