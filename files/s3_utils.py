import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

def get_s3_object_url(bucket_name, file_key, expiration_time=3600):
    try:
        s3 = get_s3_client()

        # Generate the URL for the S3 object
        object_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_key}, ExpiresIn=expiration_time)

        return object_url

    except NoCredentialsError:
        print("Credentials not available")
        return None