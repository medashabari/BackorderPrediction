import os, sys
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from backorder.entity import config_entity
from backorder.components.data_ingestion import DataIngestion
from backorder.components.data_validation import DataValidation
from backorder.components.data_transformation import DataTransformation
from backorder.components.model_trainer import ModelTrainer
from backorder.components.model_evaluation import ModelEvaluation
from backorder.components.model_pusher import ModelPusher
import warnings
warnings.filterwarnings('ignore')
def start_training_pipeline():
     try:
        # creaing training pipeline config
        training_pipeline_config =  config_entity.TrainingPipelineConfig()

        # creaing DataIngestionConfig
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)

        #DataIngestionObject
        data_ingestion = DataIngestion(data_ingestion_config)

        #Initiating DataIngestionArtifacts and retrieving DataIngetionArtifacts
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        #DataValidationConfig
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)

        #DataValidation Object
        data_validation = DataValidation(data_validation_config, data_ingestion_artifact)

        #Initiating DataValidation and retriving DataValidation Artifacts
        data_validation_artifact = data_validation.initiate_data_validation()

        #DataTransformationConfig
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config)

        #DataTransformation Object
        data_transformation = DataTransformation(data_ingestion_artifact, data_transformation_config)

        #Initiating DataTransformation and retriving DataTransformation Artifacts
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        #ModelTrainerConfig
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config)

        #ModelTrainer Object
        model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)

        #Initiating ModelTrainer and retriving ModelTrainer Artifacts
        model_trainer_artifact = model_trainer.initiate_model_training()

        #ModelEvaluationConfig
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config)

        #ModelEvaluation Object
        model_evaluation = ModelEvaluation(model_eval_config, data_ingestion_artifact, data_transformation_artifact, model_trainer_artifact)

        #Initiating ModelEvaluation and retriving ModelEvaluation Artifacts
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
        
        #ModelPusher Config
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)

        #ModelPusher Object
        model_pusher = ModelPusher(model_pusher_config, data_transformation_artifact, model_trainer_artifact)

        #Initiating ModelPusher and retriving ModelPusher Artifacts
        model_pusher_artifact = model_pusher.initiate_model_pusher()

     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)