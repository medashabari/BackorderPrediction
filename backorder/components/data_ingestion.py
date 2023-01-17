import os,sys 
from backorder.exception import BackOrderException 
from backorder.logger import logging
from backorder.entity import config_entity,artifact_entity
from backorder import utils

from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class DataIngestion:
    """
    Description: DataIngestion Class
    """
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info("==============================================================")
            logging.info("================Started DataIngestion ========================")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            BackOrderException(error=e, error_detail=sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        """
        Description: Function returns DataIngestionArtifacts

        Returns:
                DataIngestionArtifacts
        """
        try:
            logging.info("================Initiating DataIngestion ========================")
            df:pd.DataFrame = utils.get_parquet_as_dataFrame(bucket_name=os.getenv('BUCKET_NAME'), filename=self.data_ingestion_config.parquet_file_name)
            logging.info("Replacing the null values with np.Nan in Dataset")

            # replacing na values np.Nan 
            df.replace(to_replace='na',value=np.nan,inplace=True)
    
            # creating feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            # Saving the dataframe to feature store folder
            logging.info('Saving the dataframe to feature store folder')
            df.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            # splitting the dataset into train and test sets
            logging.info('splitting the dataset into train and test sets')
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            # creating dataset folders for train and test sets if not available 
            logging.info("creating dataset folders for train and test sets if not available ")
            dataset_train_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_train_dir,exist_ok=True)
            dataset_test_dir =  os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dataset_test_dir,exist_ok=True)

            # Saving train and test set dataframe to train and test set folders
            logging.info("Saving train and test set dataframe to train and test set folders")
            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            # Preparing the DataIngestion Artifacts

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path, 
                train_file_path = self.data_ingestion_config.train_file_path, test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data Ingestion Artifact {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            BackOrderException(error=e, error_detail=sys)