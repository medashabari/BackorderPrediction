from backorder.exception import BackOrderException
from backorder.pipeline.training_pipeline import start_training_pipeline
import os,sys 

try:
    start_training_pipeline()
except Exception as e:
    raise BackOrderException(error=e, error_detail=sys)