import aioboto3
from fastapi import UploadFile
from datetime import datetime, timezone
from ..core.config import settings
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION

def get_s3_client():
    return aioboto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url="http://localhost:4566",
    )

async def ensure_bucket_exists(bucket_name: str):
    async with get_s3_client() as s3:
        try:
            await s3.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                await s3.create_bucket(Bucket=bucket_name)

async def upload_file(file_obj: UploadFile, bucket_name: str):
    await ensure_bucket_exists(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename_with_timestamp = f"{timestamp}_{file_obj.filename}"

    async with get_s3_client() as s3:
        await s3.upload_fileobj(file_obj.file, bucket_name, filename_with_timestamp)

    return f"/{filename_with_timestamp}"

async def delete_file(filename: str, bucket_name: str):
    await ensure_bucket_exists(bucket_name)

    async with get_s3_client() as s3:
        await s3.delete_object(Bucket=bucket_name, Key=filename)

        try:
            await s3.head_object(Bucket=bucket_name, Key=filename)
            raise Exception(f"File {filename} still exists after delete attempt.")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return {"message": f"{filename} deleted from {bucket_name}"}
            else:
                raise Exception(f"Unexpected error while verifying file deletion: {str(e)}")

async def update_file(existing_filename: str, file_obj: UploadFile, bucket_name: str):
    await delete_file(existing_filename, bucket_name)
    return await upload_file(file_obj, bucket_name)