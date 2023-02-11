from backorder.entity.config_entity import MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_FILE_NAME,TRANSFORMER_OBJECT_FILE_NAME,CATEGORICAL_ENCODER_OBJECT_FILE_NAME
from backorder.exception import BackOrderException
from backorder.logger import logging
import os,sys
import glob
from typing import Optional

class ModelResolver:
    """
    Description: This class solves the model selection problem
    """
    def __init__(self,model_registry:str='saved_models',
                transformer_dir_name:str='transformer',
                categorical_encoder_dir_name:str='categorical_encoder',
                target_encoder_dir_name:str='target_encoder',
                model_dir_name:str='model'):
        
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.categorical_encoder_dir_name = categorical_encoder_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name
    
    def get_latest_dir_path(self)->Optional[str]:
        """
        Description : This funtion returns latest trained directory
        ----------------------------------------------------------------
        Returns:
           latest trained directory path
           returns none if there is no trained model
        """
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                logging.info(f"There are no trained models")
                return None
            dir_names = list(map(int,dir_names))
            lateset_dir_name = max(dir_names)
            logging.info(f"Latest directory path {self.model_registry}/{lateset_dir_name}")
            return os.path.join(self.model_registry,f"{lateset_dir_name}")

        except Exception as e:
            raise e

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.info("Model is not available")
                raise Exception("Model is not available")
            logging.info(f"Latest model path {os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_PATH)}")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_PATH)
        except Exception as e:
            raise e

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.info("Transformer is not available")
                raise Exception("Transformer is not available")
            logging.info(f"Latest Transfomer path {os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_PATH)}")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
        
    def get_latest_categorical_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.info("Transformer is not available")
                raise BackOrderException(error="Transformer is not available",error_detail=sys)
            logging.info(f"Latest categotical encoder path {os.path.join(latest_dir,self.model_dir_name,CATEGORICAL_ENCODER_OBJECT_FILE_NAME)}")
            return os.path.join(latest_dir,self.model_dir_name,CATEGORICAL_ENCODER_OBJECT_FILE_NAME) 
        except Exception as e:
            raise e
    
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.info("Target encoder is not available")
                raise BackOrderException(error="Target encoder is not available",error_detail=sys)
            logging.info(f"Latest Target encoder path {os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)}")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_dir_path(self)->str:
        """
        Description: This function returns latest saving directory path to save the latest training model
        Returns:
            returns latest saving directory path to save the latest training model
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir==None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise e
    
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            logging.info(f"Latest saving model path {os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_PATH)}")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_PATH)
        except Exception as e:
            raise e

    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            logging.info(f"Latest saving transforming path {os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)}")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
    def get_latest_save_categorical_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            logging.info(f"Latest save categorical encoder path {os.path.join(latest_dir,self.categorical_encoder_dir_name,CATEGORICAL_ENCODER_OBJECT_FILE_NAME)}")
            return os.path.join(latest_dir,self.categorical_encoder_dir_name,CATEGORICAL_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            logging.info(f"Latest save target encoder path {os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)}")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e