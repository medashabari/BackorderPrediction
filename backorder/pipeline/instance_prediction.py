from backorder.exception import BackOrderException

from backorder.utils import load_object
from backorder.model_resolving import ModelResolver
from datetime import datetime
from backorder.utils import TARGET_COLUMN
import os,sys 
import pandas as pd 
import numpy as np

def instance_prediction(input_dict)->str:
    try:
        df = pd.DataFrame(data=[input_dict.values()],columns=input_dict.keys())
        model_resolver = ModelResolver(model_registry='saved_models')
        numerical_transformer = load_object(model_resolver.get_latest_transformer_path())
        input_feature_names1 = numerical_transformer.feature_names_in_
        df[input_feature_names1] = numerical_transformer.transform(df[input_feature_names1])

        catergorical_transformer = load_object(model_resolver.get_latest_categorical_encoder_path())
        input_feature_names2 = catergorical_transformer.feature_names_in_
        df[input_feature_names2] = catergorical_transformer.transform(df[input_feature_names2])
        model = load_object(model_resolver.get_latest_model_path())
        ypred = model.predict(df)
        targer_encoder = load_object(model_resolver.get_latest_target_encoder_path())    
        return targer_encoder.inverse_transform(ypred.astype(int))  
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)
