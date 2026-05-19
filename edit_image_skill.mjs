// Vertex AI Edit Image Skill
// usage: node edit_image_skill.mjs <image_path> <prompt> <output_path>
import { GoogleAuth } from 'google-auth-library';
import fs from 'fs';
import fetch from 'node-fetch';

const args = process.argv.slice(2);
if (args.length < 3) {
  console.log("Usage: node edit_image_skill.mjs <image_path> <prompt> <output_path>");
  process.exit(1);
}
const [imagePath, prompt, outputPath] = args;

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
    
    if (!fs.existsSync(imagePath)) {
        console.error("Original image not found at path:", imagePath);
        return;
    }
    const imageBytes = fs.readFileSync(imagePath, 'base64');
    
    const payload = {
      instances: [
        {
          prompt: prompt,
          image: { bytesBase64Encoded: imageBytes }
        }
      ],
      parameters: {
        sampleCount: 1,
        personGeneration: "ALLOW_ALL",
        editConfig: {
            editMode: "product-image" // can be changed to inpainting-insert or inpainting-remove if mask is provided
        }
      }
    };
    
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
