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
          prompt: { stringValue: "A beautiful anime style scene: A mischievous blue cat wearing a tiny red scarf tries to catch a shimmering golden fish swimming in a floating water bubble, magical atmosphere, vibrant colors, Studio Ghibli inspired, high quality 4k animation" }
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
  
  const videoBytes = response.video?.bytesBase64 || response.bytesBase64 || response.predictions?.[0]?.structValue?.fields?.videoBase64?.stringValue || response.predictions?.[0]?.structValue?.fields?.bytesBase64?.stringValue;
  
  if (videoBytes) {
      fs.writeFileSync('/home/gateman/.openclaw/workspace/veo_blue_cat.mp4', Buffer.from(videoBytes, 'base64'));
      console.log("Saved to veo_blue_cat.mp4");
  } else {
      console.log(JSON.stringify(response, null, 2).substring(0, 1000));
  }
}

main().catch(console.error);
