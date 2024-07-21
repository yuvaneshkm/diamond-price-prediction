# Importing necessary libraries:
import os
from pathlib import Path
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

            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.join(os.path.dirname(script_dir), "../")
            artifacts_dir = os.path.join(base_dir, "artifacts")

            preprocessor_path = Path(artifacts_dir) / "preprocessor.pkl"
            model_path = Path(artifacts_dir) / "model.pkl"

            # loading preprocessor and model:
            logging.info("Loading Preprocessor and Model object")
            data_preprocessor = load_object(preprocessor_path)
            logging.info("Preprocessor Object Loaded")
            ml_model = load_object(model_path)
            logging.info("Model object loaded")

            logging.info("Data Preprocessing")
            preprocessed_diamond_detail = data_preprocessor.transform(diamond_detail)
            logging.info(f"Preprocessing completed:\n{preprocessed_diamond_detail}")
            logging.info("Diamond Price Prediction")
            predicted_price = ml_model.predict(preprocessed_diamond_detail)
            logging.info(f"The Predicted price is {predicted_price[0]}")

        except Exception as ex:
            raise CustomException(ex)

        return predicted_price
