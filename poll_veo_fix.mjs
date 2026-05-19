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

  // Fix the URL format for Operations API in Vertex AI
  const operationName = 'projects/jason-hsbc/locations/us-central1/publishers/google/models/veo-2.0-generate-001/operations/6cfa2d84-2633-4998-8615-fcb6f87837ea';
  // Correct endpoint for polling operations is on the location
  const url = `https://us-central1-aiplatform.googleapis.com/v1/${operationName}`;

  try {
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
      }
    });
    
    // Log raw text if not JSON
    const text = await res.text();
    try {
        const data = JSON.parse(text);
        console.log(`Operation done: ${data.done}`);
        if (data.done && data.response && data.response.predictions) {
            const videoBytes = data.response.predictions[0]?.bytesBase64;
            if (videoBytes) {
                fs.writeFileSync('/home/gateman/.openclaw/workspace/blue_cat.mp4', Buffer.from(videoBytes, 'base64'));
                console.log("Video saved to /home/gateman/.openclaw/workspace/blue_cat.mp4");
            } else {
                console.log("No bytesBase64 found.");
            }
        } else if (data.done && data.error) {
            console.error("Error payload:", data.error);
        } else if (!data.done) {
            console.log("Still processing...");
        } else {
            console.log("Unexpected data:", data);
        }
    } catch(e) {
        console.log("Response was not JSON. Status:", res.status);
        console.log("Body preview:", text.substring(0, 500));
    }
  } catch (e) {
    console.error(e);
  }
}

main();
