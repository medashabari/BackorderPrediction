import os, sys 
from backorder.entity import config_entity, artifact_entity 
from backorder.logger import logging 
from backorder.exception import BackOrderException 
from backorder import utils 
import pandas as pd
import numpy as np 
from scipy.stats import ks_2samp


class DataValidation:
    """
    Description : Performs data validation operations
        - checks for columns in base and current dataframe
        - checks for data drift in base and current dataframe
    """

    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info('============================= Data validation ===============================')
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_errors = dict()
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)

    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        """
        Description : Checks wheather the Base dataframe and current Dataframe contains same columns or not
        Params :
            base_df : base dataframe
            current_df : current dataframe
            report_key_name = report name if required columns not exists
        Returns :
            Boolean values
            True if required columns exists else False
        """
        try:
            base_df_columns = base_df.columns
            current_df_columns = current_df.columns

            missing_columns = []

            for col in base_df_columns:
                if col not in current_df_columns:
                    logging.info("Columns {col} is not available in current dataframe")
                    missing_columns.append(col)
            
            if len(missing_columns)>0:
                self.validation_errors[report_key_name]=missing_columns
                return False

            return True

        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)
    
    def perform_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        """
        Description : Checks wheather any data drift in base and current Dataframes
        Params :
            base_df : base dataframe
            current_df : current dataframe
            report_key_name = report name if required columns not exists
        Returns :
            No return value
        """
        try:
            drift_report = dict()
            base_df_columns = base_df.columns
            current_df_columns = current_df.columns

            
            for base_col in base_df_columns:

                base_data,current_data = base_df[base_col],current_df[base_col]

                # Null hypothesis : The data drawn from both distributions are same

                logging.info(f'Hypothesis {base_col} and Datatypes are {base_data.dtype} {current_data.dtype}')

                same_distribution = ks_2samp(data1=base_data, data2=current_data)

                if same_distribution.pvalue > 0.05:

                    # we fail to reject the null hypothesis and the distributions are same
                    logging.info("we fail to reject the null hypothesis and the distributions are same")
                    drift_report[base_col]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    # we are rejecting the null hypothesis and the distributions are different
                    logging.info("we are rejecting the null hypothesis and the distributions are different")
                    drift_report[base_col]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }

            self.validation_errors[report_key_name]=drift_report  
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)

    def initiate_data_validation(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info('Starting Data Validation')
            logging.info('Reading the base Dataframe')
            base_df = pd.read_parquet(self.data_validation_config.base_file_path)
            # replace na with np.nan in base datafram
            logging.info("replace na with np.nan in base df")
            base_df.replace('na',np.nan,inplace=True)
            # dropping duplicates in base dataframe
            logging.info("dropping duplicates in base dataframe")
            base_df.drop_duplicates(inplace=True)

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            numerical_features_base_df = utils.return_numerical_features(base_df)
            numerical_features_train_df = utils.return_numerical_features(train_df)
            numerical_features_test_df = utils.return_numerical_features(test_df)
            logging.info(f'Numerical features in base dataframe {numerical_features_base_df}')
            logging.info(f'Numerical features in train dataframe {numerical_features_train_df}')
            logging.info(f'Numerical features in base dataframe {numerical_features_test_df}')
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.perform_data_drift(base_df=base_df[numerical_features_base_df], current_df=train_df[numerical_features_train_df],report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.perform_data_drift(base_df=base_df[numerical_features_base_df], current_df=test_df[numerical_features_test_df],report_key_name="data_drift_within_test_dataset")


            logging.info("Writing Yaml file")
            logging.info(f"Yaml file path {self.data_validation_config.report_file_path}")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path, data=self.validation_errors)

            data_validation_artifact = artifact_entity.DatavalidationArtifact(self.data_validation_config.report_file_path)
            logging.info(f'Data validation artifact {data_validation_artifact}')
            return data_validation_artifact


        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)