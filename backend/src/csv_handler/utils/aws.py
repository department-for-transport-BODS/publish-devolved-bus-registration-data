from os import getenv
import boto3
from botocore.exceptions import ClientError
from central_config import AWS_REGION, BUCKET_NAME, PROJECT_ENV
from .logger import log
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



class ClamAVClient:
    def __init__(self, file_name, data):
        if not BUCKET_NAME:
            raise Exception("Bucket name is not set.")
        self.bucket_name = BUCKET_NAME
        self.s3_folder = PROJECT_ENV if PROJECT_ENV != 'local' else 'dev'
        self.file_name = file_name
        self.data = data
        self.scan_file(self.bucket_name, self.s3_folder, self.file_name, self.data)


    async def scan_file(self, bucket_name,s3_folder, file_name, data):
        self.upload_bstring_to_S3_as_file(bucket_name,s3_folder, file_name, data)
        print(f"File {file_name} is uploaded to S3 bucket {bucket_name}.")
        for i in range(1,11):
            sleep(10)
            res = self.read_file_tags(bucket_name,s3_folder, file_name)
            if res is not None:
                log.info(f"Getting tags is done, after {i} attempts.")
                self.delete_file_from_s3(bucket_name,s3_folder, file_name)
                log.info(f"File {file_name} is deleted from S3 bucket.")
                break
            print(f"Attempt {i} to get tags is not successful.")
        av_status = [item['Value'] for item in res if item['Key'] == 'av-status']

        if len(av_status) > 0:
            if av_status[0] == 'clean':
                return 
                
        
        raise Exception("File did not pass antivirus check.")


    def get_boto_client(self):
        boto3.setup_default_session(profile_name='AWSPowerUserAccess-992382470170')
        return boto3.client(service_name='s3',region_name=AWS_REGION,)

        


    def upload_bstring_to_S3_as_file(
            self,bucket_name, s3_folder,file_name, binary_data
            ) -> None:
        try:
            client = self.get_boto_client()
            
            # Specify the bucket name and the key (including another filename)
            object_key = f'{s3_folder}/{file_name}.csv'

            # # Upload the binary data
            client.put_object(Body=binary_data, Bucket=bucket_name, Key=object_key)
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception(f'Errors: Could not upload file to S3.')


    def read_file_tags(self,bucket_name,s3_folder, file_name):
        try:
            # Initialize the S3 client
            client = self.get_boto_client()
            # Get the object tagging
            object_key = f'{s3_folder}/{file_name}.csv'
            print(f"Reading tags for file {object_key}.")
            response = client.get_object_tagging(Bucket=bucket_name, Key=object_key)

            # 'TagSet': [{'Key': 'scanned-by', 'Value': 'ClamAV'}, {'Key': 'av-status', 'Value': 'clean'}]
            # Return the tags
            if response is not None:
                tag_set = response.get('TagSet')
                if tag_set and len(tag_set) > 0:
                    return tag_set
            
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception('Errors: Could not read file tags from S3.')
        

    def delete_file_from_s3(self, bucket_name,s3_folder, file_name):
        try:
            # Initialize the S3 client
            client = self.get_boto_client()
            # Delete the object
            object_key = f'{s3_folder}/{file_name}.csv'
            client.delete_object(Bucket=bucket_name, Key=object_key)
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception('Errors: Could not delete file from S3.')


# if __name__ == '__main__':
    # print(os.getcwd())
    # file_name = 'test5'
    # bucket_name = 'shared-pdbrd-clamav-artefacts-992382470170'
    # data = b'test data'
    # ClamAVClient(file_name, data)