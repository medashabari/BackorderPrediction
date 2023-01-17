import os
import boto3
client = boto3.client('s3')
def upload_files(file_name,bucket,object_name=None,args=None):
    """
    file_name: name of the file you want to upload
    bucket: bucket_name
    object_name: name of file on s3
    args: custom args
    """

    if object_name is None:
        object_name = file_name
    
    response=client.upload_file(file_name,bucket,object_name,ExtraArgs=args)
    if response==None:
        return "Successfully Uploaded"
upload_files(file_name='/config/workspace/sample_bo.parquet.gzip',bucket=os.getenv("BUCKET_NAME"),object_name="sample_bo.parquet.gzip")