# Importing necessary libraries:
import os
import sys
from pathlib import Path
from typing import List
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictionPipeline:

    def __init__(self):
        pass

    def predict(self, features:pd.DataFrame):
        try:
            # path of the preprocessor and the model:
            preprocessor_path = Path(
                os.path.abspath(os.path.join(os.getcwd(), "../../artifacts/preprocessor.pkl"))
            )
            model_path = Path(
                os.path.abspath(os.path.join(os.getcwd(), "../../artifacts/model.pkl"))
            )

            # loading the preprocessor and the model:
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            preprocessed_features = preprocessor.transform(features)
            predicted_price = model.predict(preprocessed_features)

        except Exception as ex:
            logging.info(CustomException(ex))
        
        return predicted_price
    

class CustomData:

    def __init__(self):
        pass

    def get_data_as_dataframe(self):
        try:
            pass
        except Exception as ex:
            logging.info(CustomData(ex))