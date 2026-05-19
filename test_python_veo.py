from google.cloud import aiplatform

aiplatform.init(project="jason-hsbc", location="us-central1")
client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})

print([m for m in dir(client) if 'long' in m.lower()])
