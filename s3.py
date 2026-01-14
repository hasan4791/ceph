import boto3
import botocore.exceptions

# Configuration
S3_ENDPOINT = 'http://localhost:8000'
ACCESS_KEY = '0555b35654ad1656d804'
SECRET_KEY = 'h7GhxuBLTrlhVUyxSPUKUV8r/2EI4ngqJxD7iBdBYLhwluN30JaT3Q=='
BUCKET_NAME = 'boto3-test-bucket'

# Create an S3 client
s3 = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    verify=False # Use verify=True if using a valid SSL certificate
)

try:
    # Create a bucket
    print(f"Creating bucket: {BUCKET_NAME}")
    s3.create_bucket(Bucket=BUCKET_NAME)

    # List buckets
    print("Listing buckets:")
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")

    # Upload an object
    print("Uploading object...")
    s3.put_object(Bucket=BUCKET_NAME, Key='test-object.txt', Body='Hello, Ceph RGW!')

    # List objects in the bucket
    print(f"Listing objects in {BUCKET_NAME}:")
    response = s3.list_objects(Bucket=BUCKET_NAME)
    for obj in response['Contents']:
        print(f"  {obj['Key']}")

except botocore.exceptions.ClientError as e:
    print(f"An S3 error occurred: {e.response['Error']['Code']}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Cleanup (optional but good practice)
    try:
        print("Cleaning up...")
        s3.delete_object(Bucket=BUCKET_NAME, Key='test-object.txt')
        s3.delete_bucket(Bucket=BUCKET_NAME)
        print("Cleanup complete.")
    except Exception:
        pass
