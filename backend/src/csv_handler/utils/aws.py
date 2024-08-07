import boto3
from central_config import AWS_REGION, BUCKET_NAME, PROJECT_ENV
from os import getenv
from time import sleep
from .logger import log


def upload_file_to_S3(
        file_path, bucket, bucket_path, local_file_name, file_name_in_s3
    ) -> None:
        """Upload a file to an S3 bucket

        Args:
            file_path (str): The path to the file to upload
            bucket (str): The name of the bucket
            bucket_path (str): The path in the bucket
            local_file_name (str): The name of the file to upload
            file_name_in_s3 (str): The name of the file in S3
        """
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


    def scan(self):
        """Initiate the scan process

        Returns:
            Boolean: True if the file is clean, False otherwise
        """
        res = self.scan_file(self.bucket_name, self.s3_folder, self.file_name, self.data)
        return res


    def scan_file(self, bucket_name, s3_folder, file_name, data):
        result = False
        """This function does the following:
        - Uploads a file to S3 via upload_bstring_to_s3_as_file function
        - Waits for the file to be scanned via added tags
        - Checks the scan status
        - Gets the scan result
        - Deletes the file from S3

        Args:
            bucket_name (str): The name of the S3 bucket
            s3_folder (str): The folder in the S3 bucket
            file_name (str): The name of the file
            data (bytes): The file data

        Returns:
            Boolean: True if the file is clean, False otherwise
        """
        try:
            self.upload_bstring_to_s3_as_file(bucket_name,s3_folder, file_name, data)
            print(f"File {file_name} is uploaded to S3 bucket {bucket_name}.")
            for i in range(1,11):
                sleep(15)
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
                    result = True
                    
        except Exception as e:
            log.error(f'Errors: {e}')
        
        finally:
            return result


    def get_boto_client(self):
        """Get the boto3 client

        Returns:
            client: The boto3 client
        """
        return boto3.client(service_name='s3',region_name=AWS_REGION,)


    def upload_bstring_to_s3_as_file(
            self,bucket_name, s3_folder, file_name, binary_data
            ) -> None:
        """Upload a binary string to S3 as a file

        Args:
            bucket_name (str): The name of the S3 bucket
            s3_folder (str): The folder in the S3 bucket
            file_name (str): The name of the file
            binary_data (bytes): The binary data to upload

        Raises:
            Exception: If the file could not be uploaded
        """
        try:
            client = self.get_boto_client()
            
            # Specify the bucket name and the key (including another filename)
            object_key = f'{s3_folder}/{file_name}.csv'

            # # Upload the binary data
            client.put_object(Body=binary_data, Bucket=bucket_name, Key=object_key)
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception(f'Errors: Could not upload file to S3.')


    def read_file_tags(self, bucket_name, s3_folder, file_name):
        """Read the tags of a file in S3

        Args:
            bucket_name (str): The name of the S3 bucket
            s3_folder (str): The folder in the S3 bucket
            file_name (str): The name of the file

        Raises:
            Exception: If the tags could not be read

        Returns:
            str: The tags of the file clean or infected 
        """
        try:
            # Initialize the S3 client
            client = self.get_boto_client()
            # Get the object tagging
            object_key = f'{s3_folder}/{file_name}.csv'
            print(f"Reading tags for file {object_key}.")
            response = client.get_object_tagging(Bucket=bucket_name, Key=object_key)

            if response is not None:
                tag_set = response.get('TagSet')
                if tag_set and len(tag_set) > 0:
                    return tag_set
            
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception('Errors: Could not read file tags from S3.')


    def delete_file_from_s3(self, bucket_name, s3_folder, file_name):
        """Delete a file from S3

        Args:
            bucket_name (str): The name of the S3 bucket
            s3_folder (str): The folder in the S3 bucket
            file_name (str): The name of the file

        Raises:
            Exception: If the file could not be deleted
        """
        try:
            # Initialize the S3 client
            client = self.get_boto_client()
            # Delete the object
            object_key = f'{s3_folder}/{file_name}.csv'
            client.delete_object(Bucket=bucket_name, Key=object_key)
        except Exception as e:
            print(f'Errors: {e}')
            raise Exception('Errors: Could not delete file from S3.')