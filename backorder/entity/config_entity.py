import os, sys 
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from datetime import datetime 

FILE_NAME = "backorder.csv"
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'
TRANSFORMER_OBJECT_FILE_NAME = 'transformer.pkl'
TARGET_ENCODER_OBJECT_FILE_NAME = 'target.pkl'
CATEGORICAL_ENCODER_OBJECT_FILE_NAME = 'categorical.pkl'
MODEL_FILE_NAME = 'model.pkl'
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
class DataTransformationConfig:
    """
    Description : Creates DataTransformation Configuration Files
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir =os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
            os.makedirs(self.data_transformation_dir,exist_ok=True)
            self.transformer_object_file_path  = os.path.join(self.data_transformation_dir,'transformer',TRANSFORMER_OBJECT_FILE_NAME)
            self.transformed_train_path = os.path.join(self.data_transformation_dir,'transformed',TRAIN_FILE_NAME.replace('csv', 'npz'))
            self.transformed_test_path = os.path.join(self.data_transformation_dir,'transformed',TEST_FILE_NAME.replace('csv', 'npz'))
            self.categorical_encoder_object_file_path = os.path.join(self.data_transformation_dir,'transformer',CATEGORICAL_ENCODER_OBJECT_FILE_NAME)
            self.target_encoder_object_file_path = os.path.join(self.data_transformation_dir,'target',TARGET_ENCODER_OBJECT_FILE_NAME)
            
            
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)


class ModelTrainerConfig:
    """
    Description : Creates Model Training Configuration Files
    """
    try:
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            self.model_train_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
            os.makedirs(self.model_train_dir,exist_ok=True)
            self.model_object_path = os.path.join(self.model_train_dir,'model',MODEL_FILE_NAME)
            self.expected_score = 0.7
            self.over_fitting_threshold = 0.1
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)
class ModelEvaluationConfig:...
class ModelPusherConfig:...
