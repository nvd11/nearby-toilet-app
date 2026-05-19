from google.oauth2 import service_account
from google.cloud import aiplatform

credentials = service_account.Credentials.from_service_account_file('/home/gateman/sa-key.json')
aiplatform.init(project="jason-hsbc", location="us-central1", credentials=credentials)
client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}, credentials=credentials)

print([m for m in dir(client) if 'long_running' in m.lower() or 'longrunning' in m.lower()])
