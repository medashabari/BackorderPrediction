import os, sys
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from backorder.pipeline import training_pipeline
import warnings
warnings.filterwarnings('ignore')
if __name__ == '__main__':
     try:
          logging.info("Initiating Training PipeLine")
          training_pipeline.start_training_pipeline()
          logging.info("Training Completed")
     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)