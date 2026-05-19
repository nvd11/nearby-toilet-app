const fs = require('fs');
const data = fs.readFileSync('nuxt.json', 'utf8');
const j = JSON.parse(data);
// Let's dump the entire json looking for urls
function walk(obj) {
    if (typeof obj === 'string' && obj.includes('http')) {
        if (obj.includes('google') || obj.includes('googleapis') || obj.includes('aiplatform')) {
            console.log(obj);
        }
    } else if (Array.isArray(obj)) {
        obj.forEach(walk);
    } else if (typeof obj === 'object' && obj !== null) {
        Object.values(obj).forEach(walk);
    }
}
walk(j);
