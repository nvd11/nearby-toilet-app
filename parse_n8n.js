const fs = require('fs');
const html = fs.readFileSync('n8n.json', 'utf8');
const match = html.match(/"nodes":\s*(\[.*?\])/s);
if (match) {
    const nodes = JSON.parse(match[1]);
    for (const node of nodes) {
        if (node.type === 'n8n-nodes-base.httpRequest') {
            console.log(node.name);
            console.log(JSON.stringify(node.parameters, null, 2));
        }
    }
} else {
    console.log("No nodes found");
}
