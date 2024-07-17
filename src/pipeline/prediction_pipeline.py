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
from dataclasses import dataclass

class DataPreparation:

    def __init__(self,carat:float,cut:str,color:str,clarity:str,depth:float,table:float,x:float,y:float,z:float):
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
        diamond_details = {
            "carat": [self.carat],
            "cut": [self.cut],
            "color": [self.color],
            "clarity": [self.clarity],
            "depth": [self.depth],
            "table": [self.table],
            "x": [self.x],
            "y": [self.y],
            "z": [self.z]
        }
        diamond_details_df = pd.DataFrame(diamond_details)
        return diamond_details_df



@dataclass
class PredictionPipelineConfig:
    pre_path = os.path.abspath(os.path.join(os.getcwd(),"../../artifacts/preprocessor.pkl"))
    mdl_path = os.path.abspath(os.path.join(os.getcwd(),"../../artifacts/model.pkl"))


class PredictionPipeline:

    def __init__(self):
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def predict(self, diamond_detail:pd.DataFrame):
        
        # preprocessor and model path:
        try:
            preprocessor_path = Path(self.prediction_pipeline_config.pre_path)
            model_path = Path(self.prediction_pipeline_config.mdl_path)

            # loading preprocessor and model:
            data_preprocessor = load_object(preprocessor_path)
            ml_model = load_object(model_path)

            preprocessed_diamond_detail = data_preprocessor.trasform(diamond_detail)
            predicted_price = ml_model.predict(preprocessed_diamond_detail)

        except Exception as ex:
            logging.info(CustomException(ex))
        
        return predicted_price
    

