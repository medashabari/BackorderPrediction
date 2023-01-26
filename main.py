import os, sys
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from backorder.entity import config_entity
from backorder.components.data_ingestion import DataIngestion
from backorder.components.data_validation import DataValidation
from backorder.components.data_transformation import DataTransformation
from backorder.components.model_trainer import ModelTrainer
if __name__ == '__main__':
     try:
          training_pipeline_config =  config_entity.TrainingPipelineConfig()

          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)

          data_ingestion = DataIngestion(data_ingestion_config)

          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)

          data_validation = DataValidation(data_validation_config, data_ingestion_artifact)

          data_validation_artifact = data_validation.initiate_data_validation()

          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config)

          data_transformation = DataTransformation(data_ingestion_artifact, data_transformation_config)

          data_transformation_artifact = data_transformation.initiate_data_transformation()

          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config)

          model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)

          model_trainer_artifact = model_trainer.initiate_model_training()


     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)