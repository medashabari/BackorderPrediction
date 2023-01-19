import os, sys 
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from datetime import datetime 

FILE_NAME = "backorder.csv"
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

class TrainingPipelineConfig:
    """
    Description: This class contain Training Pipeline configuration.
    """
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifacts",f"{datetime.now().strftime('%d_%m_%y__%H_%M_%S')}")

        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)

class DataIngestionConfig:
    """
    Description: Creates DataIngestion Configuration Files.
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.bucket_name = os.getenv('BUCKET_NAME')
            self.parquet_file_name = 'sample_bo.parquet.gzip'

            self.data_ingestion_dir =  os.path.join(training_pipeline_config.artifact_dir,'data_ingestion')
            os.makedirs(self.data_ingestion_dir, exist_ok=True)

            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,'FEATURE_STORE',FILE_NAME)

            self.train_file_path = os.path.join(self.data_ingestion_dir,'DATASET',TRAIN_FILE_NAME)

            self.test_file_path = os.path.join(self.data_ingestion_dir,'DATASET',TEST_FILE_NAME)

            self.test_size = 0.33


        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)

            
class DataValidationConfig:
    """
    Description : Creates DataValidation Configuration files
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,'data_validation')
            os.makedirs(self.data_validation_dir,exist_ok=True)
            self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
            self.base_file_path = os.path.join('/config/workspace/sample_bo.parquet.gzip')
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
