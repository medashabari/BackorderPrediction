import os, sys
from backorder.exception import BackOrderException 
from backorder.logger import logging 
from backorder.entity import config_entity
from backorder.components.data_ingestion import DataIngestion
if __name__ == '__main__':

     training_pipeline_config =  config_entity.TrainingPipelineConfig()

     data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)

     data_ingestion = DataIngestion(data_ingestion_config)

     data_ingestion_artifact = data_ingestion.initiate_data_ingestion()