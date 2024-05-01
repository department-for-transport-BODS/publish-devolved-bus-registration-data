import boto3
from botocore.exceptions import ClientError
# from central_config import AWS_REGION
# from .logger import log, console
from time import sleep

def get_secret(secret_name: str):
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=AWS_REGION,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("The requested secret " + secret_name + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            print("The request was invalid due to:", e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            print("The request had invalid params:", e)
        elif e.response["Error"]["Code"] == "DecryptionFailure":
            print(
                "The requested secret can't be decrypted using the provided KMS key:", e
            )
        elif e.response["Error"]["Code"] == "InternalServiceError":
            print("An error occurred on service side:", e)
    else:
        if "SecretString" in get_secret_value_response:
            text_secret_data = get_secret_value_response["SecretString"]
            return {"text_secret_data": text_secret_data}
        # else:
        #     binary_secret_data = get_secret_value_response['SecretBinary']
        #     return {"binary_secret_data": binary_secret_data}


def upload_file_to_S3(
        file_path, bucket, bucket_path, local_file_name, file_name_in_s3
    ) -> None:
        try:
            # Connect to aws s3
            s3 = boto3.resource('s3')

            # Compile bucket path and file name to generate key
            key = f'{bucket_path}/{file_name_in_s3}'

            # Compile full path of the uploaded file
            file_full_path = f'{file_path}/{local_file_name}'

            # Upload the file to s3 bucket
            s3.meta.client.upload_file(file_full_path, bucket, key)
            

            # Check if the file exists
            client = boto3.client('s3')
            client.head_object(Bucket=bucket, Key=key)
        except Exception as e:
            log.error(f'Errors: {e}')

def upload_bstring_to_S3_as_file(
           bucket_name, binary_data, file_name
        ) -> None:
    try:
        boto3.setup_default_session(profile_name='AWSPowerUserAccess-992382470170')
        # Initialize the S3 client
        client = boto3.client(
            service_name='s3',
            )

        # Specify the bucket name and the key (including another filename)
        object_key = f'dev/{file_name}.csv'

        # # Upload the binary data
        client.put_object(Body=binary_data, Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(f'Errors: {e}')
        raise Exception(f'Errors: Could not upload file to S3.')


def read_file_tags(bucket_name, file_name):
    try:
        # Initialize the S3 client
        boto3.setup_default_session(profile_name='AWSPowerUserAccess-992382470170')
        client = boto3.client('s3')

        # Get the object tagging
        object_key = f'dev/{file_name}.csv'
        response = client.get_object_tagging(Bucket=bucket_name, Key=object_key)

        # 'TagSet': [{'Key': 'scanned-by', 'Value': 'ClamAV'}, {'Key': 'av-status', 'Value': 'clean'}]
        # Return the tags
        tag_set = response.get('TagSet')
        if tag_set and len(tag_set) > 0:
            return tag_set
        
    except Exception as e:
        print(f'Errors: {e}')
        raise Exception('Errors: Could not read file tags from S3.')
    

def delete_file_from_s3(bucket_name, file_name):
    try:
        # Initialize the S3 client
        boto3.setup_default_session(profile_name='AWSPowerUserAccess-992382470170')
        client = boto3.client('s3')

        # Delete the object
        object_key = f'dev/{file_name}.csv'
        client.delete_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(f'Errors: {e}')
        raise Exception('Errors: Could not delete file from S3.')


if __name__ == '__main__':
    file_name = 'test5'
    bucket_name = 'shared-pdbrd-clamav-artefacts-992382470170'
    data = b'test data'
    def check_file(bucket_name,file_name, data):
        upload_bstring_to_S3_as_file(bucket_name, data, file_name)
        print(f"File {file_name} is uploaded to S3 bucket {bucket_name}.")
        for i in range(1,11):
            sleep(10)
            res = read_file_tags(bucket_name, file_name)
            if res is not None:
                print(f"Getting tags is done, after {i} attempts.")
                print(res)
                delete_file_from_s3(bucket_name, file_name)
                print(f"File {file_name} is deleted from S3 bucket {bucket_name}.")
                break
            print(f"Attempt {i} to get tags is not successful.")


        av_status = [item['Value'] for item in res if item['Key'] == 'av-status']
        if len(av_status) > 0:
            print(f"File is {av_status[0]}.")