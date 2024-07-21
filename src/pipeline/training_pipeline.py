# Importing necessary packages
from pathlib import Path
from src.components import (
    data_ingestion,
    data_transformation,
    model_trainer,
    model_evaluation,
)
import warnings

warnings.filterwarnings("ignore")


# Data Ingestion
diobj = data_ingestion.DataIngestion()
raw_data_path, train_data_path, test_data_path = diobj.initiate_data_ingestion()

raw_path = Path(raw_data_path)
train_path = Path(train_data_path)
test_path = Path(test_data_path)

# Data Transformation
dtobj = data_transformation.DataTransformation()
preprocessed_train_df, preprocessed_test_df = dtobj.initiate_data_transformation(
    raw_path, train_path, test_path
)

# Model Training
mtobj = model_trainer.ModelTrainer()
mtobj.initiate_model_training(preprocessed_train_df, preprocessed_test_df, raw_path)

# Model Evaluation:
meobj = model_evaluation.ModelEvaluation()
meobj.initiate_model_evaluation(preprocessed_test_df)
