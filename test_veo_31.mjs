import { GoogleAuth } from 'google-auth-library';
import fetch from 'node-fetch';

async function main() {
  const auth = new GoogleAuth({
    keyFilename: '/home/gateman/sa-key.json',
    scopes: ['https://www.googleapis.com/auth/cloud-platform'],
  });
  const client = await auth.getClient();
  const token = await client.getAccessToken();

  const projectId = 'jason-hsbc';
  const location = 'us-central1';
  const model = 'veo-3.1-generate-preview';
  
  const url = `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/publishers/google/models/${model}:predictLongRunning`;
  
  const payload = {
    instances: [
        {
            prompt: "A beautiful anime style scene: A mischievous blue cat wearing a tiny red scarf tries to catch a shimmering golden fish swimming in a floating water bubble, magical atmosphere, vibrant colors, Studio Ghibli inspired, high quality 4k animation"
        }
    ],
    parameters: {
        aspectRatio: "16:9",
        personGeneration: "allow_adult"
    }
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log(`Status (${model}): ${res.status}`);
    console.log(JSON.stringify(data, null, 2));
  } catch (e) {
    console.error(e);
  }
}

main();
