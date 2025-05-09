import logging
import os
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class AWSHelper:
    """
    Helper class for AWS operations that provides functionality for interacting with various AWS services.
    """
    
    def __init__(self, region: Optional[str] = None, 
                 access_key_id: Optional[str] = None,
                 secret_access_key: Optional[str] = None,
                 session_token: Optional[str] = None,
                 endpoint_url: Optional[str] = None):
        """
        Initialize the AWS helper with credentials and region.
        
        Args:
            region: AWS region (defaults to environment variable AWS_REGION)
            access_key_id: AWS access key ID (defaults to environment variable AWS_ACCESS_KEY_ID)
            secret_access_key: AWS secret access key (defaults to environment variable AWS_SECRET_ACCESS_KEY)
            session_token: AWS session token for temporary credentials (defaults to environment variable AWS_SESSION_TOKEN)
            endpoint_url: Custom endpoint URL for AWS services (e.g., for localstack)
        """
        try:
            import boto3
            self.boto3 = boto3
        except ImportError:
            logger.error("boto3 library not found. Please install it with 'pip install boto3'")
            raise ImportError("boto3 library not found. Please install it with 'pip install boto3'")
        
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.access_key_id = access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_access_key = secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        self.session_token = session_token or os.getenv('AWS_SESSION_TOKEN')
        self.endpoint_url = endpoint_url or os.getenv('AWS_ENDPOINT_URL')
        
        # Session for AWS operations
        self.session = self._create_session()
        
        # Cache for AWS clients
        self._clients = {}

    def _create_session(self):
        """
        Create a boto3 session with the provided credentials.
        
        Returns:
            A boto3 Session object
        """
        try:
            # Create session with credentials if provided
            if self.access_key_id and self.secret_access_key:
                logger.info(f"Creating AWS session with provided credentials in region {self.region}")
                session_kwargs = {
                    'aws_access_key_id': self.access_key_id,
                    'aws_secret_access_key': self.secret_access_key,
                    'region_name': self.region
                }
                
                if self.session_token:
                    session_kwargs['aws_session_token'] = self.session_token
                    
                return self.boto3.Session(**session_kwargs)
            else:
                # Create session using environment variables or IAM role
                logger.info(f"Creating AWS session with environment credentials in region {self.region}")
                return self.boto3.Session(region_name=self.region)
        except Exception as e:
            logger.error(f"Failed to create AWS session: {str(e)}")
            raise

    def _get_client(self, service_name: str) -> Any:
        """
        Get a boto3 client for the specified service.
        
        Args:
            service_name: The name of the AWS service
            
        Returns:
            A boto3 client for the specified service
        """
        # Check if client is already cached
        if service_name in self._clients:
            return self._clients[service_name]
        
        # Create a new client
        client_kwargs = {}
        if self.endpoint_url:
            client_kwargs['endpoint_url'] = self.endpoint_url
            
        try:
            client = self.session.client(service_name, **client_kwargs)
            self._clients[service_name] = client
            return client
        except Exception as e:
            logger.error(f"Failed to create AWS client for {service_name}: {str(e)}")
            raise

    def _get_resource(self, service_name: str) -> Any:
        """
        Get a boto3 resource for the specified service.
        
        Args:
            service_name: The name of the AWS service
            
        Returns:
            A boto3 resource for the specified service
        """
        resource_kwargs = {}
        if self.endpoint_url:
            resource_kwargs['endpoint_url'] = self.endpoint_url
            
        try:
            return self.session.resource(service_name, **resource_kwargs)
        except Exception as e:
            logger.error(f"Failed to create AWS resource for {service_name}: {str(e)}")
            raise

    # S3 Operations
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all S3 buckets.
        
        Returns:
            A list of bucket information dictionaries
        """
        try:
            s3_client = self._get_client('s3')
            response = s3_client.list_buckets()
            return response.get('Buckets', [])
        except Exception as e:
            logger.error(f"Failed to list S3 buckets: {str(e)}")
            raise

    def create_bucket(self, bucket_name: str, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new S3 bucket.
        
        Args:
            bucket_name: The name of the bucket to create
            region: The AWS region in which to create the bucket (defaults to the session region)
            
        Returns:
            The response from the S3 create_bucket operation
        """
        s3_client = self._get_client('s3')
        bucket_region = region or self.region
        
        try:
            # If region is us-east-1, we can't specify a LocationConstraint
            if bucket_region == 'us-east-1':
                return s3_client.create_bucket(Bucket=bucket_name)
            else:
                return s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': bucket_region}
                )
        except Exception as e:
            logger.error(f"Failed to create S3 bucket {bucket_name}: {str(e)}")
            raise

    def delete_bucket(self, bucket_name: str, force: bool = False) -> Dict[str, Any]:
        """
        Delete an S3 bucket.
        
        Args:
            bucket_name: The name of the bucket to delete
            force: If True, delete all objects in the bucket before deleting the bucket
            
        Returns:
            The response from the S3 delete_bucket operation
        """
        s3_client = self._get_client('s3')
        
        try:
            if force:
                self.delete_all_objects(bucket_name)
                
            return s3_client.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            logger.error(f"Failed to delete S3 bucket {bucket_name}: {str(e)}")
            raise

    def list_objects(self, bucket_name: str, prefix: str = '') -> List[Dict[str, Any]]:
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: The name of the bucket
            prefix: The prefix to filter objects by
            
        Returns:
            A list of object information dictionaries
        """
        s3_client = self._get_client('s3')
        
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            return response.get('Contents', [])
        except Exception as e:
            logger.error(f"Failed to list objects in S3 bucket {bucket_name}: {str(e)}")
            raise

    def upload_file(self, local_path: str, bucket_name: str, s3_key: str, extra_args: Optional[Dict[str, Any]] = None) -> None:
        """
        Upload a file to an S3 bucket.
        
        Args:
            local_path: The path to the local file
            bucket_name: The name of the bucket
            s3_key: The key to use for the object in S3
            extra_args: Extra arguments to pass to the upload operation
        """
        s3_client = self._get_client('s3')
        
        try:
            logger.info(f"Uploading file {local_path} to s3://{bucket_name}/{s3_key}")
            s3_client.upload_file(local_path, bucket_name, s3_key, ExtraArgs=extra_args)
        except Exception as e:
            logger.error(f"Failed to upload file to S3: {str(e)}")
            raise

    def download_file(self, bucket_name: str, s3_key: str, local_path: str, extra_args: Optional[Dict[str, Any]] = None) -> None:
        """
        Download a file from an S3 bucket.
        
        Args:
            bucket_name: The name of the bucket
            s3_key: The key of the object in S3
            local_path: The path to save the file locally
            extra_args: Extra arguments to pass to the download operation
        """
        s3_client = self._get_client('s3')
        
        try:
            logger.info(f"Downloading file s3://{bucket_name}/{s3_key} to {local_path}")
            s3_client.download_file(bucket_name, s3_key, local_path, ExtraArgs=extra_args)
        except Exception as e:
            logger.error(f"Failed to download file from S3: {str(e)}")
            raise

    def delete_object(self, bucket_name: str, s3_key: str) -> Dict[str, Any]:
        """
        Delete an object from an S3 bucket.
        
        Args:
            bucket_name: The name of the bucket
            s3_key: The key of the object to delete
            
        Returns:
            The response from the S3 delete_object operation
        """
        s3_client = self._get_client('s3')
        
        try:
            logger.info(f"Deleting object s3://{bucket_name}/{s3_key}")
            return s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
        except Exception as e:
            logger.error(f"Failed to delete object from S3: {str(e)}")
            raise

    def delete_all_objects(self, bucket_name: str, prefix: str = '') -> None:
        """
        Delete all objects in an S3 bucket.
        
        Args:
            bucket_name: The name of the bucket
            prefix: The prefix to filter objects by
        """
        s3_resource = self._get_resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        
        try:
            logger.info(f"Deleting all objects in bucket {bucket_name} with prefix '{prefix}'")
            bucket.objects.filter(Prefix=prefix).delete()
        except Exception as e:
            logger.error(f"Failed to delete all objects from S3 bucket {bucket_name}: {str(e)}")
            raise

    # This class can be extended with methods for other AWS services 
    # such as DynamoDB, SQS, Lambda, etc. as needed
