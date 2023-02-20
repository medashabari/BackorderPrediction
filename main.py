import os, sys
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from backorder.pipeline import training_pipeline
from backorder.pipeline.batch_prediction import start_batch_prediction
import warnings
warnings.filterwarnings('ignore')
if __name__ == '__main__':
     try:
          logging.info("Initiating Training PipeLine")
          training_pipeline.start_training_pipeline()
          logging.info("Training Completed")
          logging.info("Batch prediction")
          print(start_batch_prediction('/config/workspace/test_bo_.parquet.gzip'))
          logging.info("Batch prediction completed")


     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)