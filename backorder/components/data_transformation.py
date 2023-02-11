from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.entity import config_entity,artifact_entity
from backorder import utils
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek
import os,sys


class DataTransformation:
    """
    Description : Performs Data transformation operations.
    """
    def __init__(self,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,data_transformation_config:config_entity.DataTransformationConfig):
        try:
            logging.info("==================================DataTransformation=============================================")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        """
        Description: Returns sklearn Pipeline object
        """
        try:
            numerical_pipeline = Pipeline(steps=[
            ('si',SimpleImputer(strategy='median')),
            ('rs',RobustScaler()),
            ])
            return numerical_pipeline
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)


    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        """
        Description : Initiates the Data transformation
        ================================================
        Returns : DataTransformation Artifact
        """
        try:
            logging.info("retriving train and test Dataframes")
            # retriving train and test Dataframes
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Making input features for train and test data
            logging.info('Making input features for train and test data')
            input_feature_train_df = train_df.drop(utils.TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(utils.TARGET_COLUMN,axis=1)

            # Target column for train and test data
            logging.info("Target column for train and test data")
            target_feature_train_df = train_df[utils.TARGET_COLUMN]
            target_feature_test_df = test_df[utils.TARGET_COLUMN]

            # label encoding the target feature
            logging.info("label encoding the target feature")
            labelencoder = LabelEncoder()
            labelencoder.fit(target_feature_train_df)

            # Transformation on target features
            logging.info('Transformation on target features')
            target_feature_train_array = labelencoder.transform(target_feature_train_df)
            target_feature_test_array = labelencoder.transform(target_feature_test_df)

            # Transformation on numerical input featues
            logging.info("Get numerical  pipeline object")
            transformation_pipeline_obj = DataTransformation.get_data_transformer_object()
            numerical_features = utils.return_numerical_features(input_feature_train_df)  
            logging.info(f"Numerical features {numerical_features}")          
            logging.info("Transformation on numerical input featues")
            input_feature_train_df[numerical_features] = transformation_pipeline_obj.fit_transform(input_feature_train_df[numerical_features])
            input_feature_test_df[numerical_features] = transformation_pipeline_obj.transform(input_feature_test_df[numerical_features])

            # Handling Categorical features

            logging.info('Handling Categorical Features')
            categorical_features = utils.return_categorical_features(input_feature_train_df)
            logging.info(f"Categorical Features {categorical_features}")
            ohe = OneHotEncoder(drop='if_binary',sparse_output=False)
            input_feature_train_df[categorical_features] = ohe.fit_transform(input_feature_train_df[categorical_features])
            input_feature_test_df[categorical_features] = ohe.transform(input_feature_test_df[categorical_features])


            input_feature_train_array = input_feature_train_df.to_numpy()
            input_feature_test_array = input_feature_test_df.to_numpy()

            # Handling the imbalance data
            logging.info("Handling the imbalance data")
            smt = SMOTETomek(random_state=42,sampling_strategy='minority')

            logging.info(f'Before resampling the shape of the training set :{input_feature_train_array.shape} Target : {target_feature_train_array.shape}')

            input_feature_train_array,target_feature_train_array = smt.fit_resample(input_feature_train_array,target_feature_train_array)

            logging.info(f'After resampling the shape of the training set :{input_feature_train_array.shape} Target : {target_feature_train_array.shape}')

            logging.info(f"Before resampling the shape of the test set : {input_feature_test_array.shape} Target : {target_feature_test_array.shape}")

            input_feature_test_array,target_feature_test_array = smt.fit_resample(input_feature_test_array,target_feature_test_array)

            logging.info(f"After resampling the shape of the test set : {input_feature_test_array.shape} Target : {target_feature_test_array.shape}")

            train_array = np.c_[input_feature_train_array,target_feature_train_array]
            test_array = np.c_[input_feature_test_array,target_feature_test_array]

            logging.info("Saving Objects")
            # Saving the numpy array
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_train_path, array=train_array)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_test_path, array=test_array)

            # Saving transformer Objects 
            utils.save_object(file_path=self.data_transformation_config.transformer_object_file_path, obj=transformation_pipeline_obj)
            utils.save_object(file_path=self.data_transformation_config.categorical_encoder_object_file_path, obj=ohe)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_object_file_path, obj=labelencoder)

            logging.info("Successfull saved the objects")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformer_object_file_path = self.data_transformation_config.transformer_object_file_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path, 
                transformed_test_path=self.data_transformation_config.transformed_test_path, 
                categorical_encoder_object_file_path=self.data_transformation_config.categorical_encoder_object_file_path,
                target_encoder_object_file_path=self.data_transformation_config.target_encoder_object_file_path)

            logging.info(f"Data Transformation Artifact {data_transformation_artifact}")

            return data_transformation_artifact
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)


        
