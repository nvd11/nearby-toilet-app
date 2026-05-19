import { GoogleAuth } from 'google-auth-library';
import fs from 'fs';
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
    
    const url = `https://${location}-aiplatform.googleapis.com/v1beta1/projects/${projectId}/locations/${location}/publishers/google/models/veo-3.1-generate-preview:predictLongRunning`;
    
    const payload = {
      instances: [
        { prompt: "A gorgeous and highly elegant female secretary walking gracefully in a modern sunlit office, cinematic lighting, ultra high quality, photorealistic, 4k resolution" }
      ],
      parameters: {
        aspectRatio: "16:9",
        personGeneration: "ALLOW_ADULT"
      }
    };

    console.log("Submitting to Veo 3.1 Preview:", url);
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
    console.log("Initial Response:", JSON.stringify(data, null, 2));

    if (data.name) {
        console.log("Operation started! ID:", data.name);
        let opName = data.name;
        let isDone = false;
        let attempts = 0;
        
        while (!isDone && attempts < 30) {
            attempts++;
            console.log(`Waiting 10s... (Attempt ${attempts})`);
            await new Promise(r => setTimeout(r, 10000));
            
            const pollUrl = `https://${location}-aiplatform.googleapis.com/v1beta1/${opName}`;
            const pollRes = await fetch(pollUrl, {
                headers: { 'Authorization': `Bearer ${token.token}` }
            });
            if (!pollRes.ok) {
                console.error("Poll Error:", await pollRes.text());
                continue;
            }
            
            const pollData = await pollRes.json();
            if (pollData.done) {
                isDone = true;
                if (pollData.error) {
                    console.error("Operation failed:", JSON.stringify(pollData.error, null, 2));
                } else if (pollData.response && pollData.response.generatedVideos && pollData.response.generatedVideos[0]) {
                    const videoBytes = pollData.response.generatedVideos[0].video.videoBytes;
                    const outPath = "/home/gateman/.openclaw/workspace/beauty_video.mp4";
                    fs.writeFileSync(outPath, Buffer.from(videoBytes, 'base64'));
                    console.log("Success! Video saved to:", outPath);
                } else {
                    console.log("Operation done but no video data:", JSON.stringify(pollData, null, 2));
                }
            }
        }
    }

  } catch (e) {
      console.error("Caught Exception:", e);
  }
}
main();