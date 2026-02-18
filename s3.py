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

def multi_delete_objects(bucket, object_keys):
# Format the keys for the boto3 delete_objects structure
    print("Deleting keys",object_keys)
    delete_list = {'Objects': [{'Key': k} for k in object_keys]}
    try:
        response = s3.delete_objects(Bucket=bucket, Delete=delete_list)

    # Check for success
        deleted = response.get('Deleted', [])
        errors = response.get('Errors', [])

        print(f"Successfully deleted {len(deleted)} objects.")
        for error in errors:
            print(f"Error deleting {error['Key']}: {error['Code']}")

    except ClientError as e:
        print(f"Client error: {e}")

try:
    # Create a bucket
    print(f"1.Creating bucket: {BUCKET_NAME}")
    s3.create_bucket(Bucket=BUCKET_NAME)

    # List buckets
    print("2.Listing buckets:")
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")

    # Upload an object
    print("3.Uploading object...")
    s3.put_object(Bucket=BUCKET_NAME, Key='test-object.txt', Body='Hello, Ceph RGWHHHHHH!!!')
    s3.put_object(Bucket=BUCKET_NAME, Key='test-object1.txt', Body='Hello, Ceph2 RGWHHHHHH!!!')
    s3.put_object(Bucket=BUCKET_NAME, Key='test-object2.txt', Body='Hello, Ceph3 RGWHHHHHH!!!')

    # List objects in the bucket
    print(f"4.Listing objects in {BUCKET_NAME}:")
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
        print("5.Deleting object...")
        keys_to_delete = ['test-object.txt', 'test-object1.txt', 'test-object2.txt']
        #keys_to_delete = ['test-object.txt']
        multi_delete_objects(bucket=BUCKET_NAME, object_keys=keys_to_delete)
        #s3.delete_object(Bucket=BUCKET_NAME, Key='test-object.txt')
        print("6.Deleting bucket...")
        s3.delete_bucket(Bucket=BUCKET_NAME)
        print("Cleanup complete.")
    except Exception as e:
    	print(f"An unexpected error occurred: {e}")
        #pass
