from backorder.model_resolving import ModelResolver
from backorder.entity.config_entity import ModelPusherConfig
from backorder.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact
import os,sys
from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.utils import save_object,load_object 

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
    data_transformation_artifact:DataTransformationArtifact,
    model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'=='*20} Model Pusher {'=='*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            logging.info(f"Loading transformer model and target encoder")

            numerical_transformer = load_object(file_path=self.data_transformation_artifact.transformer_object_file_path)
            categorical_transformer = load_object(file_path=self.data_transformation_artifact.categorical_encoder_object_file_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_object_file_path)
            model = load_object(file_path=self.model_trainer_artifact.model_file_path)

            # model pusher dir
            logging.info(f"Saving model into model pusher directory")
            save_object(file_path=self.model_pusher_config.pusher_numerical_transfomer_path, obj=numerical_transformer)
            save_object(file_path=self.model_pusher_config.pusher_categorical_transformer_path, obj=categorical_transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path,obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_path, obj=target_encoder)

            # saved model dir
            logging.info(f"Saving model in saved model dir")
            numerical_transformer_path = self.model_resolver.get_latest_save_transformer_path()
            categorical_transformer_path = self.model_resolver.get_latest_save_categorical_encoder_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()
            model_path = self.model_resolver.get_latest_save_model_path()

            save_object(file_path=numerical_transformer_path, obj=numerical_transformer)
            save_object(file_path=categorical_transformer_path, obj=categorical_transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
            saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact


        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)