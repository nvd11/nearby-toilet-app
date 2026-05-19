const fs = require('fs');
async function run() {
    const res = await fetch("https://docs.getbifrost.ai/providers/supported-providers/vertex");
    console.log((await res.text()).substring(0, 1000));
}
run();
