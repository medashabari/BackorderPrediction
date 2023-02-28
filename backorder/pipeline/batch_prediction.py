from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.utils import load_object
from backorder.model_resolving import ModelResolver
from datetime import datetime
from backorder.utils import TARGET_COLUMN
import os,sys 
import pandas as pd 
import numpy as np
PREDICTION_DIR = 'predictions'

def start_batch_prediction(url = None ,input_file_path='sample_bo.parquet.gzip'):
    try:
        logging.info("Creating Model resolver Object")
        model_resolver = ModelResolver(model_registry='saved_models')
        logging.info(f"Input file name {input_file_path}")
        df = pd.read_parquet(url)
        logging.info(f"Shape of the data set {df.shape}")

        logging.info("Replacing the null values with np.Nan in Dataset")
        df.replace(to_replace='na',value=np.nan,inplace=True)
        df.dropna(thresh=10,inplace=True)
        logging.info("Handling unusaul values in 2 columns")
        df['perf_6_month_avg'].replace({-99:np.nan},inplace=True)
        df['perf_12_month_avg'].replace({-99:np.nan},inplace=True)

        logging.info("Loading the numerical transformer")
        numerical_transformer = load_object(model_resolver.get_latest_transformer_path())
        input_feature_names1 = numerical_transformer.feature_names_in_
        df[input_feature_names1] = numerical_transformer.transform(df[input_feature_names1])

        logging.info("Loading the categorical Transformer")
        catergorical_transformer = load_object(model_resolver.get_latest_categorical_encoder_path())
        input_feature_names2 = catergorical_transformer.feature_names_in_
        df[input_feature_names2] = catergorical_transformer.transform(df[input_feature_names2])
        
        logging.info("Loading the latest Model")

        model = load_object(model_resolver.get_latest_model_path())
        logging.info('predicting using the latest model')
        ypred = model.predict(df.drop(TARGET_COLUMN,axis=1))
    
        logging.info("Loading the target encoder")
        targer_encoder = load_object(model_resolver.get_latest_target_encoder_path())        
        pred = targer_encoder.inverse_transform(ypred.astype(int))

        df[input_feature_names2] = catergorical_transformer.inverse_transform(df[input_feature_names2])
        df['prediction'] = ypred
        df['cat_prediction'] = pred
        prediction_file_name = os.path.basename(input_file_path).replace(".parquet.gzip",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path  = os.path.join(PREDICTION_DIR,prediction_file_name)
        #df.to_csv(prediction_file_path,index=False,header=True)
        return df,prediction_file_path 
        
        
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)
