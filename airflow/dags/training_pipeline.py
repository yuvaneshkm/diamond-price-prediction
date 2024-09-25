from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.pipeline import training_pipeline

training_pipeline_obj = training_pipeline()

with DAG()
