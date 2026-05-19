import { GoogleAuth } from 'google-auth-library';
import fs from 'fs';
import fetch from 'node-fetch';

const args = process.argv.slice(2);
if (args.length < 2) {
  console.log("Usage: node generate_image_skill.mjs <prompt> <output_path>");
  process.exit(1);
}
const [prompt, outputPath] = args;

const auth = new GoogleAuth({
  keyFile: '/home/gateman/sa-key.json',
  scopes: ['https://www.googleapis.com/auth/cloud-platform'],
});

async function main() {
  try {
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    const projectId = 'jason-hsbc';
    const location = 'us-central1';
    
    const payload = {
      instances: [
        {
          prompt: prompt
        }
      ],
      parameters: {
        sampleCount: 1,
        personGeneration: "ALLOW_ALL",
        aspectRatio: "1:1"
      }
    };
    
    // For pure generation, we use a different URL/model than edit:
    // https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images
    const url = `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/publishers/google/models/imagen-3.0-generate-001:predict`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        console.error("API Error Response:", await response.text());
        return;
    }
    const data = await response.json();
    if (data.predictions && data.predictions[0] && data.predictions[0].bytesBase64Encoded) {
        fs.writeFileSync(outputPath, Buffer.from(data.predictions[0].bytesBase64Encoded, 'base64'));
        console.log(`Success! Image saved as ${outputPath}`);
    } else {
        console.error("Success response but no image data found:", JSON.stringify(data, null, 2));
    }
  } catch (e) {
      console.error("Caught Exception:", e);
  }
}
main();