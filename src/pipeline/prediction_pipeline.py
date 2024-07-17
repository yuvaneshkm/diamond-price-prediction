# Importing necessary libraries:
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class DataPreparation:

    def __init__(
        self,
        carat: float,
        cut: str,
        color: str,
        clarity: str,
        depth: float,
        table: float,
        x: float,
        y: float,
        z: float,
    ):
        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z

    def custom_data(self) -> pd.DataFrame:
        logging.info("Data Preparation Started")
        diamond_details = {
            "carat": [self.carat],
            "cut": [self.cut],
            "color": [self.color],
            "clarity": [self.clarity],
            "depth": [self.depth],
            "table": [self.table],
            "x": [self.x],
            "y": [self.y],
            "z": [self.z],
        }
        diamond_details_df = pd.DataFrame(diamond_details)
        logging.info(f"Details are converted into a DataFrame:\n{diamond_details_df}")

        return diamond_details_df


class PredictionPipeline:

    def __init__(self):
        logging.info("Prediction Pipeline Initiated")

    def predict(self, diamond_detail: pd.DataFrame):

        # preprocessor and model path:
        try:
            preprocessor_name = "preprocessor.pkl"
            model_name = "model.pkl"

            # loading preprocessor and model:
            logging.info("Loading Preprocessor and Model object")
            data_preprocessor = load_object(preprocessor_name)
            logging.info("Preprocessor Object Loaded")
            ml_model = load_object(model_name)
            logging.info("Model object loaded")

            logging.info("Data Preprocessing")
            preprocessed_diamond_detail = data_preprocessor.transform(diamond_detail)
            logging.info("Diamond Price Prediction")
            predicted_price = ml_model.predict(preprocessed_diamond_detail)
            logging.info(f"The Predicted price is {predicted_price[0]}")

        except Exception as ex:
            logging.info(CustomException(ex))

        return predicted_price
