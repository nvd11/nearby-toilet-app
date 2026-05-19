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

  // The operation ID from the previous response
  const operationName = 'projects/jason-hsbc/locations/us-central1/publishers/google/models/veo-3.1-generate-preview/operations/07a1b6d9-2b1c-4080-81d0-73e0f13c9586';
  // Correct endpoint for polling operations in Vertex AI is on the location endpoint
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
    try {
        const data = JSON.parse(text);
        console.log(`Operation done: ${data.done}`);
        if (data.done && data.response && data.response.predictions) {
            const videoBytes = data.response.predictions[0]?.bytesBase64 || data.response.predictions[0]?.video?.bytesBase64;
            if (videoBytes) {
                fs.writeFileSync('/home/gateman/.openclaw/workspace/blue_cat_31.mp4', Buffer.from(videoBytes, 'base64'));
                console.log("Video saved to /home/gateman/.openclaw/workspace/blue_cat_31.mp4");
            } else {
                console.log("No bytesBase64 found.", JSON.stringify(data.response.predictions[0]).substring(0, 200));
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
