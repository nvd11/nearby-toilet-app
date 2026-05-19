const fs = require('fs');
async function run() {
    const key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ";
    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            contents: [{ parts: [{ text: "In Google Cloud Vertex AI, when I call the `predictLongRunning` REST API for `veo-3.1-generate-preview`, it returns an operation name like `projects/my-project/locations/us-central1/publishers/google/models/veo-3.1-generate-preview/operations/5b6c1d3f-bbbc-4288-beab-484ecd6cb7ed`. What EXACT HTTP GET URL do I use to poll this operation's status using curl? Do I use the generic operations endpoint or something else? If I use generic it says 'must be a Long' for operations endpoint. Show me the exact curl URL to get the video response." }] }]
        })
    });
    const result = await res.json();
    console.log(result.candidates[0].content.parts[0].text);
}
run();
