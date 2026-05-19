import { GoogleAuth } from 'google-auth-library';
import fetch from 'node-fetch';
import fs from 'fs';

async function main() {
  const auth = new GoogleAuth({
    keyFilename: '/home/gateman/sa-key.json',
    scopes: ['https://www.googleapis.com/auth/cloud-platform'],
  });
  const client = await auth.getClient();
  const token = await client.getAccessToken();

  const operationName = 'projects/jason-hsbc/locations/us-central1/publishers/google/models/veo-2.0-generate-001/operations/6cfa2d84-2633-4998-8615-fcb6f87837ea';
  const url = `https://us-central1-aiplatform.googleapis.com/v1/${operationName}`;

  try {
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
      }
    });

    const text = await res.text();
    console.log(`Status: ${res.status}`);
    console.log(`Response text length: ${text.length}`);
    try {
        const data = JSON.parse(text);
        console.log(`Operation done: ${data.done}`);
        if (data.done) {
          if (data.error) {
            console.error("Error:", data.error);
          } else if (data.response && data.response.predictResponse && data.response.predictResponse.predictions) {
            const videoBytes = data.response.predictResponse.predictions[0]?.bytesBase64;
            if (videoBytes) {
              fs.writeFileSync('/home/gateman/.openclaw/workspace/blue_cat.mp4', Buffer.from(videoBytes, 'base64'));
              console.log("Video saved to /home/gateman/.openclaw/workspace/blue_cat.mp4");
            } else {
              console.log("No video bytes found in response.");
            }
          }
        } else {
          console.log("Still rendering...");
        }
    } catch(e) {
        console.log(text.substring(0, 200));
    }
  } catch (e) {
    console.error(e);
  }
}

main();
