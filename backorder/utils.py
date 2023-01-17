import pandas as pd 
import os,sys
from backorder.exception import BackOrderException
from backorder.logger import logging

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
        s3 = boto3.resource('s3')
        bucket=s3.Bucket(bucket_name)
        files=list(bucket.objects.all())
        for file in files:
            if file.key==filename:
                logging.info(f"Dowloading the file {filename}.")
                client.download_file(bucket_name,file.key,file.key)
                logging.info('Reading File')
                df = pd.read_parquet(filename)
                logging.info(f'Shape of the dataset {df.shape}')
                logging.info(f'Columns found \n {df.columns}')
                return df
    except Exception as e:
        BackOrderException(error=e, error_detail=sys)
