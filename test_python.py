import google.auth
from google.cloud import aiplatform

credentials, project = google.auth.load_credentials_from_file("/home/gateman/sa-key.json")

aiplatform.init(project="jason-hsbc", location="us-central1", credentials=credentials)

# Let's get the operation
client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})
# Wait, PredictionServiceClient doesn't have get_operation.
# We need to use OperationsClient maybe? Wait, OperationsClient is from google.longrunning

from google.longrunning import operations_pb2
from google.longrunning import operations_pb2_grpc
import grpc

channel = grpc.secure_channel('us-central1-aiplatform.googleapis.com:443', grpc.ssl_channel_credentials())
stub = operations_pb2_grpc.OperationsStub(channel)

# Wait, we need to pass credentials in the grpc channel.
# Instead of doing that manually, just use aiplatform sdk.
