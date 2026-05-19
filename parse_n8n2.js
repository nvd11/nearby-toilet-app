const fs = require('fs');
async function run() {
    const res = await fetch("https://n8n.io/workflows/5228-generate-video-from-prompt-using-vertex-ai-veo-3-and-upload-to-google-drive/");
    const html = await res.text();
    const match = html.match(/id="__NUXT_DATA__">(.+?)<\/script>/);
    if (match) {
        fs.writeFileSync('nuxt.json', match[1]);
        console.log("Found NUXT_DATA");
    }
}
run();
