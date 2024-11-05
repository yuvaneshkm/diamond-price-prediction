# importing necessary libraries:
import os
from pathlib import Path
import pandas as pd
from src.utils import load_object
import mlflow
import mlflow.pyfunc as fn
from src.exception import CustomException
import warnings

warnings.filterwarnings("ignore")


class PredictionPipeline:
    def __init__(self):
        pass

    def x(self, input_data: pd.DataFrame) -> pd.DataFrame:
        try:
            pre_path = os.path.join("artifacts", "preprocessor.pkl")
            preprocessor_path = Path(pre_path)
            preprocessor_object = load_object(preprocessor_path)

            preprocessed_input_data = preprocessor_object.transform(input_data)

        except Exception as ex:
            raise CustomException(ex)

        return preprocessed_input_data

    def y(self, input_data: pd.DataFrame) -> str:
        try:
            preprocessed_data = self.x(input_data=input_data)

            remote_server_uri = (
                "https://dagshub.com/yuvaneshkm/diamond-price-prediction.mlflow"
            )
            mlflow.set_tracking_uri(remote_server_uri)

            model_name = "diamond-price-predictor"

            model_object = fn.load_model(model_uri=f"models:/{model_name}/Production")

            price = model_object.predict(preprocessed_data)
            predicted_price = str(round(price[0], 2))

        except Exception as ex:
            raise CustomException(ex)

        return predicted_price


if __name__ == "__main__":

    data_dict = {
        "carat": [float("0.32")],
        "cut": [str("Ideal")],
        "color": [str("G")],
        "clarity": [str("VS1")],
        "depth": [float("61.6")],
        "table": [float("56.0")],
        "x": [float("4.38")],
        "y": [float("4.41")],
        "z": [float("2.71")],
    }

    df = pd.DataFrame(data_dict)
    prediction_pipe_obj = PredictionPipeline()
    price_ = prediction_pipe_obj.y(df)
    print(price_)
