import pandas as pd 
import numpy as np
import os,sys
from backorder.exception import BackOrderException
from backorder.logger import logging
import boto3
import yaml
from typing import List
import dill

TARGET_COLUMN = 'went_on_backorder'

def get_parquet_as_dataFrame(bucket_name:str,filename:str)->pd.DataFrame:
    """ 
    Description : This funtion returns thre parquet file dumped from s3 as DataFrame
    ===============================================================================
    Params:
        filename : Parquet filename
    --------------------------------------------------------------------------------
    returns:
        Pandas Dataframe
    
    """
    try:
        client = boto3.client('s3')
        logging.info(f"Dowloading the file {filename} from s3.")
        client.download_file(bucket_name,filename,filename)
        logging.info('Reading File')
        df = pd.read_parquet("/config/workspace/"+filename)
        logging.info(f'Shape of the dataset {df.shape}')
        logging.info(f'Columns found \n {df.columns}')
        return df
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)
    
def return_numerical_features(dataset)->List:
    """
    Description : Returns list of numerical features in the dataframe
    Params: Pandas Dataframe
    ==========================================================
    Returns : List of numerical features in the input dataframe
    """
    
    try:
        numerical_features =[feature for feature in dataset.columns if dataset[feature].dtype !='O']
        return numerical_features
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)

def return_categorical_features(dataset)->List:
    """
    Description : Returns list of numerical features in the dataframe
    Params: Pandas Dataframe
    ==========================================================
    Returns : List of numerical features in the input dataframe
    """
    try:
        categorical_features = [feature for feature in dataset.columns if dataset[feature].dtype=='O']
        return categorical_features
    except Exception as e:
        raise BackOrderException(error=e, error_detail=e)



def write_yaml_file(file_path,data:dict)->None:
    """
    Description: Writes the dictionary data into the Yaml File
    Params : File path to write the Yaml file
    ===========================================================
    Return : None
    """
    
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)

        with open(file_path, "w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)


def save_object(file_path:str,obj:object)->None:
    """
    Description : Saves the object file into the input file path.
    Params :
        file_path:str
        obj : object
    ===============================================================
    Returns None
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_writer:
            dill.dump(obj,file_writer)
        logging.info('Successfully saved the object')
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)

def load_object(file_path:str)->object:
    """
    Description : Loads the Object file from the input file path
    Params :
        file_path:str
    ===============================================================
    Returns file object:object
    """
    try:
        if not os.path.exists(file_path):
            raise BackOrderException(error=f"The file path {file_path} does not exists", error_detail=sys)
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)

def save_numpy_array(file_path:str,array:np.array)->None:
    """
    Description : Saves the numpy array into the input file path.
    Params :
        file_path:str
        array:np.array
    ===============================================================
    Returns None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_writer:
            np.save(file_writer,array)
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)

def load_numpy_array(file_path:str)->np.array:
    """
    Description : Loads the numpy array from the input file path
    Params :
        file_path:str
    ===============================================================
    Returns array:np.array
    """
    try:
        if not os.path.exists(file_path):
            raise BackOrderException(error=f"The file path {file_path} does not exists", error_detail=sys)
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise BackOrderException(error=e, error_detail=sys)
