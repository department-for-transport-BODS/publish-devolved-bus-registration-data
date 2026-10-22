import boto3
import json
from botocore.config import Config
from central_config import AWS_REGION, BUCKET_NAME, PROJECT_ENV
from os import environ
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
        s3 = boto3.resource("s3")

        # Compile bucket path and file name to generate key
        key = f"{bucket_path}/{file_name_in_s3}"

        # Compile full path of the uploaded file
        file_full_path = f"{file_path}/{local_file_name}"

        # Upload the file to s3 bucket
        s3.meta.client.upload_file(file_full_path, bucket, key)

        # Check if the file exists
        client = boto3.client("s3")
        client.head_object(Bucket=bucket, Key=key)
    except Exception as e:
        log.error(f"Errors: {e}")


class ClamAVClient:
    """Stages a file in the shared ClamAV bucket, where the scanner tags it with av-status."""

    POLL_INTERVAL_SECONDS = 2
    MAX_POLLS = 75

    def __init__(self, file_name):
        if not BUCKET_NAME:
            raise Exception("Bucket name is not set.")
        self.bucket_name = BUCKET_NAME
        s3_folder = PROJECT_ENV if PROJECT_ENV != "local" else "dev"
        self.object_key = f"{s3_folder}/{file_name}.csv"
        self.client = boto3.client(service_name="s3", region_name=AWS_REGION)

    def upload(self, data: bytes) -> None:
        self.client.put_object(Body=data, Bucket=self.bucket_name, Key=self.object_key)

    def wait_until_clean(self) -> bool:
        """Poll the scanner's tags. False if infected or no verdict before the deadline."""
        for attempt in range(1, self.MAX_POLLS + 1):
            tags = self.client.get_object_tagging(
                Bucket=self.bucket_name, Key=self.object_key
            ).get("TagSet", [])
            av_status = next((t["Value"] for t in tags if t["Key"] == "av-status"), None)
            if av_status is not None:
                log.info(f"ClamAV verdict for {self.object_key} after {attempt} polls: {av_status}")
                return av_status == "clean"
            sleep(self.POLL_INTERVAL_SECONDS)
        log.error(f"No ClamAV verdict for {self.object_key} after {self.MAX_POLLS} polls")
        return False

    def read(self) -> bytes:
        return self.client.get_object(Bucket=self.bucket_name, Key=self.object_key)["Body"].read()

    def delete(self) -> None:
        self.client.delete_object(Bucket=self.bucket_name, Key=self.object_key)


def invoke_this_lambda_async(payload: dict) -> None:
    """Fire-and-forget invocation of the running Lambda with a custom event."""
    client = boto3.client(
        "lambda",
        region_name=AWS_REGION,
        config=Config(connect_timeout=5, read_timeout=10, retries={"max_attempts": 2}),
    )
    client.invoke(
        FunctionName=environ["AWS_LAMBDA_FUNCTION_NAME"],
        InvocationType="Event",
        Payload=json.dumps(payload).encode(),
    )
