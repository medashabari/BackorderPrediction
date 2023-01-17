import os
import boto3
import pandas as pd

def Getdatas3(filename)->pd.DataFrame:
    s3 = boto3.resource('s3')
    bucket=s3.Bucket(os.getenv("BUCKET_NAME"))
    files=list(bucket.objects.all())
    for file in files:
        if file.key==filename:
            client.download_file(os.getenv("BUCKET_NAME"),file.key,file.key)
            df = pd.read_parquet(filename)
            return df
