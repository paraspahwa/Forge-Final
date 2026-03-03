"""
Cloud storage service (R2/S3 compatible)
"""

import uuid
from typing import Optional
from datetime import datetime, timedelta

import boto3
from botocore.config import Config

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class StorageService:
    """Service for cloud storage operations"""
    
    def __init__(self):
        self.client = None
        self.resource = None
        self._init_client()
    
    def _init_client(self):
        """Initialize S3-compatible client"""
        try:
            session = boto3.session.Session()
            
            self.client = session.client(
                "s3",
                region_name=settings.R2_REGION,
                endpoint_url=settings.R2_ENDPOINT_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                config=Config(
                    retries={"max_attempts": 3, "mode": "standard"},
                    connect_timeout=10,
                    read_timeout=30,
                ),
            )
            
            self.resource = session.resource(
                "s3",
                region_name=settings.R2_REGION,
                endpoint_url=settings.R2_ENDPOINT_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            )
            
            logger.info("Storage client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize storage client: {e}")
            raise
    
    async def upload_file(
        self,
        file_path: str,
        destination_path: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload file to storage
        
        Returns:
            Public URL of uploaded file
        """
        if destination_path is None:
            destination_path = f"{uuid.uuid4()}/{file_path.split('/')[-1]}"
        
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        
        try:
            self.client.upload_file(
                file_path,
                settings.R2_BUCKET_NAME,
                destination_path,
                ExtraArgs=extra_args,
            )
            
            public_url = f"{settings.R2_PUBLIC_URL}/{destination_path}"
            logger.info(f"Uploaded file to {public_url}")
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise
    
    async def upload_bytes(
        self,
        data: bytes,
        destination_path: str,
        content_type: Optional[str] = "application/octet-stream",
    ) -> str:
        """Upload bytes to storage"""
        try:
            extra_args = {"ContentType": content_type}
            
            self.client.put_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=destination_path,
                Body=data,
                **extra_args,
            )
            
            public_url = f"{settings.R2_PUBLIC_URL}/{destination_path}"
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to upload bytes: {e}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            self.client.delete_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=file_path,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    async def get_presigned_url(
        self,
        file_path: str,
        expiration: int = 3600,
        operation: str = "get_object",
    ) -> str:
        """
        Generate presigned URL for temporary access
        
        Args:
            file_path: Path to file
            expiration: URL expiration in seconds
            operation: S3 operation (get_object, put_object, etc.)
        """
        try:
            url = self.client.generate_presigned_url(
                operation,
                Params={"Bucket": settings.R2_BUCKET_NAME, "Key": file_path},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise


# Singleton instance
storage_service = StorageService()