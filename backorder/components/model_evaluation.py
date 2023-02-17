from backorder.entity import config_entity,artifact_entity 
from backorder.model_resolving import ModelResolver 
from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.utils import load_object,TARGET_COLUMN
from sklearn.metrics import f1_score
import pandas as pd
import os,sys


class ModelEvaluation:
    def __init__(self,
    model_eval_confing:config_entity.ModelEvaluationConfig,
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact,
    model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'=='*20} Model Evaluation {'=='*20}")
            self.model_eval_confing = model_eval_confing
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        """
        Description: This function initiates model evaluation
        Returns :
            ModeEvaluationArtifacts
        """

        try:
            # Checking for saved model folder to compare with the currently trained model
            logging.info("Checking for saved model folder to compare with the currently trained model")
            logging.info("Evaluating the model")
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path is None:
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model evaluation artifact {model_evaluation_artifact}")
                return model_evaluation_artifact
            # Finding the location of numerical transformer object,categorical encoder object and target encoder
            logging.info("Finding the location of numerical transformer object,categorical encoder object and target encoder")
            numerical_transformer_path = self.model_resolver.get_latest_transformer_path()
            categorical_transformer_path = self.model_resolver.get_latest_categorical_encoder_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            logging.info("Loading the previous objects")
            numerical_transformer = load_object(numerical_transformer_path)
            categorical_transformer = load_object(categorical_transformer_path)
            model = load_object(model_path)
            target_encoder = load_object(target_encoder_path)

            logging.info("Loading currently trained model objects")

            current_numerical_transformer = load_object(file_path=self.data_transformation_artifact.transformer_object_file_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_file_path)
            current_categorical_transformer = load_object(file_path=self.data_transformation_artifact.categorical_encoder_object_file_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_object_file_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_encoder.transform(target_df)
            input_numerical_features = list(numerical_transformer.feature_names_in_)
            input_categorical_features  = list(categorical_transformer.feature_names_in_)

            test_df[input_numerical_features] = numerical_transformer.transform(test_df[input_numerical_features])
            test_df[input_categorical_features] = categorical_transformer.transform(test_df[input_categorical_features])

            input_arr = test_df[input_numerical_features+input_categorical_features].to_numpy()
            logging.info("predicting using previous model")
            y_pred = model.predict(input_arr)
            previous_model_score = f1_score(y_true,y_pred,average='macro')
            logging.info(f"accuracy using previously trained model {previous_model_score}")

            # current accuracy
            test_df1 = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df1 = test_df1[TARGET_COLUMN]
            y_true1 = current_target_encoder.transform(target_df1)

            input_numerical_features1 = list(current_numerical_transformer.feature_names_in_)
            input_categorical_features1  = list(current_categorical_transformer.feature_names_in_)

            test_df1[input_numerical_features1] = current_numerical_transformer.transform(test_df1[input_numerical_features1])
            test_df1[input_categorical_features1] = current_categorical_transformer.transform(test_df1[input_categorical_features1])

            input_arr1 = test_df1[input_numerical_features1+input_categorical_features1].to_numpy()
            logging.info("predicting using current model")
            y_pred1 = current_model.predict(input_arr1)

            current_model_score = f1_score(y_true1,y_pred1,average='macro')
            logging.info(f"accuracy using current trained model {current_model_score}")

            if current_model_score <= previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")
            
            model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model EValuation artifact : {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)


