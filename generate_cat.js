const fs = require('fs');

async function main() {
  const { GoogleAuth } = require('google-auth-library');
  const auth = new GoogleAuth({
    keyFile: '/home/gateman/sa-key.json',
    scopes: 'https://www.googleapis.com/auth/cloud-platform',
  });
  const client = await auth.getClient();
  const accessToken = (await client.getAccessToken()).token;
  
  const projectId = 'jason-hsbc';
  const location = 'us-central1';
  const modelId = 'veo-3.1-generate-preview';
  
  const url = `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/publishers/google/models/${modelId}:predictLongRunning`;
  
  const payload = {
    instances: [
      {
        prompt: "High-quality anime style, Studio Ghibli inspired. A chubby blue cat with big curious eyes sits by a crystal clear fishbowl, watching a glowing golden fish gracefully swimming inside. Warm sunlight streaming through a window, magical and peaceful atmosphere, highly detailed, 4k."
      }
    ],
    parameters: {
      aspectRatio: "16:9",
      personGeneration: "allow_adult"
    }
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  
  const data = await response.json();
  console.log(JSON.stringify(data, null, 2));
}

main().catch(console.error);
