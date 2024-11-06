# Importing necessary libraries
from flask import Flask, render_template, request
import pandas as pd
from src.pipeline import prediction_pipeline
import warnings

warnings.filterwarnings("ignore")

# Creating the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        carat = request.form["carat"]
        cut = request.form["cut"]
        color = request.form["color"]
        clarity = request.form["clarity"]
        depth = request.form["depth"]
        table = request.form["table"]
        x = request.form["x"]
        y = request.form["y"]
        z = request.form["z"]

        # Building prediction data dictionary
        prediction_data_dict = {
            "carat": [float(carat)],
            "cut": [str(cut)],
            "color": [str(color)],
            "clarity": [str(clarity)],
            "depth": [float(depth)],
            "table": [float(table)],
            "x": [float(x)],
            "y": [float(y)],
            "z": [float(z)],
        }

        # Preparing data for prediction
        prediction_data = pd.DataFrame(prediction_data_dict)
        prediction_pipe_obj = prediction_pipeline.PredictionPipeline()

        # Making a prediction
        price = prediction_pipe_obj.y(prediction_data)  # Ensure this method name is correct

        return render_template("result.html", price=price)

    # In case of GET request, show the form again
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
