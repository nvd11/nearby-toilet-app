const { google } = require('googleapis');
const aiplatform = google.aiplatform('v1');
const { GoogleAuth } = require('google-auth-library');

async function main() {
  const auth = new GoogleAuth({
    keyFile: '/home/gateman/sa-key.json',
    scopes: 'https://www.googleapis.com/auth/cloud-platform',
  });
  const client = await auth.getClient();
  google.options({auth: client});
  
  const opName = 'projects/jason-hsbc/locations/us-central1/publishers/google/models/veo-3.1-generate-preview/operations/5b6c1d3f-bbbc-4288-beab-484ecd6cb7ed';
  
  console.log("Fetching operation:", opName);
  
  // Let's list operations maybe?
  try {
      const res = await aiplatform.projects.locations.operations.get({
          name: opName
      });
      console.log(res.data);
  } catch (e) {
      console.error(e.message);
  }
}
main().catch(console.error);
