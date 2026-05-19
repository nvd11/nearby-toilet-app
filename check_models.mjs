import { GoogleAuth } from 'google-auth-library';
import fetch from 'node-fetch';

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
    
    const url = `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/publishers/google/models`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}` // using token directly for simplicity, if it's a string. if object, token.token
      }
    });
    
    const data = await response.json();
    if (data.models) {
        const names = data.models.map(m => m.name.split('/').pop());
        const suspicious = names.filter(n => n.toLowerCase().includes('nano') || n.toLowerCase().includes('banana'));
        console.log("Suspicious models found:", suspicious);
        console.log("Total models listed:", names.length);
        console.log("Sample models:", names.slice(0, 10));
    } else {
        console.error("No models found or error:", JSON.stringify(data).substring(0, 500));
    }
  } catch (e) {
      console.error("Caught Exception:", e);
  }
}
main();