import pandas as pd 
import os,sys
from backorder.exception import BackOrderException
from backorder.logger import logging
import boto3
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
        BackOrderException(error=e, error_detail=sys)