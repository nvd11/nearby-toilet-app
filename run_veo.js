const { PredictionServiceClient } = require('@google-cloud/aiplatform');
const fs = require('fs');

async function main() {
  const client = new PredictionServiceClient({
    apiEndpoint: 'us-central1-aiplatform.googleapis.com',
    keyFilename: '/home/gateman/sa-key.json'
  });
  
  const projectId = 'jason-hsbc';
  const location = 'us-central1';
  const model = 'veo-3.1-generate-preview';
  const endpoint = `projects/${projectId}/locations/${location}/publishers/google/models/${model}`;
  
  console.log("Starting prediction for", endpoint);
  
  const [operation] = await client.predictLongRunning({
    endpoint: endpoint,
    instances: [{
      structValue: {
        fields: {
          prompt: { stringValue: "A cute dog running in a sunny park, highly detailed, 4k." }
        }
      }
    }],
    parameters: {
      structValue: {
        fields: {
          aspectRatio: { stringValue: "16:9" },
          personGeneration: { stringValue: "allow_adult" }
        }
      }
    }
  });
  
  console.log("Operation name:", operation.name);
  
  console.log("Waiting for operation to complete...");
  const [response] = await operation.promise();
  
  console.log("Operation finished.");
  
  // The response contains the video
  const videoBytes = response.video?.bytesBase64 || response.bytesBase64;
  if (videoBytes) {
      fs.writeFileSync('veo_video_sdk.mp4', Buffer.from(videoBytes, 'base64'));
      console.log("Saved to veo_video_sdk.mp4");
  } else {
      console.log(JSON.stringify(response, null, 2).substring(0, 1000));
  }
}

main().catch(console.error);
