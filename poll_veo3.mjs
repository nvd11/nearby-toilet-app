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

  const operationId = '6cfa2d84-2633-4998-8615-fcb6f87837ea';
  const url = `https://us-central1-aiplatform.googleapis.com/v1/projects/jason-hsbc/locations/us-central1/operations/${operationId}`;

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
          } else if (data.response) {
            fs.writeFileSync('/home/gateman/.openclaw/workspace/blue_cat.json', JSON.stringify(data.response));
            console.log("Saved response JSON.");
          }
        }
    } catch(e) {
        console.log("Not JSON");
    }
  } catch (e) {
    console.error(e);
  }
}

main();
