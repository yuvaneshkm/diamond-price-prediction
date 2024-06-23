# importing necessary libraries:
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


# creating list of files and folders inside the workspace:
list_of_files = [

    '.github/workflows/.gitkeep', # makes us to push the empty folder to github.

    # source code folder:
    'src/__init__.py',
    # exception handling:
    'src/exception/__init__.py',
    'src/exception/exception.py',
    # logger:
    'src/logger/__init__.py',
    'src/logger/logging.py',
    # source ----- components
    'src/components/__init__.py',
    'src/components/data_ingestion.py',
    'src/components/data_transformation.py',
    'src/components/model_trainer.py',
    'src/components/model_evaluation.py',
    # source ----- pipeline
    'src/pipeline/__init__.py',
    'src/pipeline/training_pipeline.py',
    'src/pipeline/prediction_pipeline.py',
    # source ----- utils
    'src/utils/__init__.py',
    'src/utils/utils.py',

    # test folder for testing
    #'tests/__init__.py',
    # test ----- unit
    'tests/unit/__init__.py',
    # test ----- integration
    'tests/integration/__init__.py',

    # setup files:
    'init_setup.sh',
    'setup.py',
    'setup.cfg',
    # requirements files:
    'requirements.txt',
    'requirements_dev.txt',
    # toml file:
    'pyproject.toml',
    # ini file:
    'tox.ini',
    # README file:
    'README.md',

    # experiment ----- notebook:
    'experiments/experiments.ipynb'

]

for filepath in list_of_files:
    # convert to os specific path:
    filepath = Path(filepath)
    # split the filepath into directory and filename:
    filedir, filename = os.path.split(filepath)

    # CREATING DIRECTORY:
    # if filedir is a non-empty string then create a directory:
    if filedir != '':
        # make the directory:
        os.makedirs(filedir, exist_ok=True)

    # CREATING FILES:
    # if the filename not exist or file size is zero then create the file:
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        # creating an empty file:
        with open(filepath, 'w') as f:
            pass
        f.close()
        