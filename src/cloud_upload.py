import boto3

def upload_to_s3(file_path, bucket_name, object_name):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_name)