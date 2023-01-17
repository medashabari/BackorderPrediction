import os,sys
import pandas as pd 

DATA_FILE_PATH ='/config/workspace/Kaggle_Training_Dataset_v2.csv'

if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(df.shape)
    df.reset_index(inplace=True,drop=True)
    #dropping the unnecessary column 
    df = df.sample(500000,random_state=42)
    df.drop('sku',inplace=True,axis=1)    
    df.to_parquet('sample_bo.parquet.gzip',compression='gzip')
