const userID = '28661606-f836-460f-87ad-1b7248a455dc';
let proxyIP = '';

if (!isValidUUID(userID)) {
    throw new Error('UUID is not valid');
}

export default {
    async fetch(request, env, ctx) {
        try {
            const uuid = env.UUID || userID;
            proxyIP = env.PROXYIP || proxyIP;
            const upgradeHeader = request.headers.get('Upgrade');
            if (!upgradeHeader || upgradeHeader !== 'websocket') {
                const url = new URL(request.url);
                switch (url.pathname) {
                    case `/${uuid}`: {
                        const vlessConfig = getVLESSConfig(userID, request.headers.get('Host'));
                        return new Response(`${vlessConfig}`, {
                            status: 200,
                            headers: {
                                "Content-Type": "text/plain;charset=utf-8",
                            }
                        });
                    }
                    default:
                        return new Response('Not found', { status: 404 });
                }
            } else {
                return await vlessOverWSHandler(request, uuid);
            }
        } catch (err) {
            return new Response(err.toString(), { status: 500 });
        }
    },
};

async function vlessOverWSHandler(request, userID) {
    const webSocketPair = new WebSocketPair();
    const [client, webSocket] = Object.values(webSocketPair);
    webSocket.accept();

    let address = '';
    let portWithRandomLog = '';
    const log = (info, event) => {
        console.log(`[${address}:${portWithRandomLog}] ${info}`, event || '');
    };
    const earlyDataHeader = request.headers.get('sec-websocket-protocol') || '';

    const readableWebSocketStream = makeReadableWebSocketStream(webSocket, earlyDataHeader, log);
    let remoteSocketWapper = { value: null };
    let isDns = false;

    readableWebSocketStream.pipeTo(new WritableStream({
        async write(chunk, controller) {
            if (isDns) { return await handleDNSQuery(chunk, webSocket, log); }
            if (remoteSocketWapper.value) {
                const writer = remoteSocketWapper.value.writable.getWriter()
                writer.write(chunk);
                writer.releaseLock();
                return;
            }

            const { hasError, message, portRemote = 443, addressRemote = '', rawDataIndex, vlessVersion = new Uint8Array([0, 0]), isUDP } = processVlessHeader(chunk, userID);
            address = addressRemote;
            portWithRandomLog = `${portRemote}--${Math.random()} ${isUDP ? 'udp ' : 'tcp '} `;
            
            if (hasError) { throw new Error(message); return; }
            if (isUDP) {
                if (portRemote === 53) { isDns = true; } else { throw new Error('UDP proxy only enable for DNS which is port 53'); }
            }

            const vlessResponseHeader = new Uint8Array([vlessVersion[0], 0]);
            const rawClientData = chunk.slice(rawDataIndex);

            if (isDns) { return await handleDNSQuery(rawClientData, webSocket, log, vlessResponseHeader); }
            handleTCPOutBound(remoteSocketWapper, addressRemote, portRemote, rawClientData, webSocket, vlessResponseHeader, log);
        },
        close() { log(`readableWebSocketStream is close`); },
        abort(reason) { log(`readableWebSocketStream is abort`, JSON.stringify(reason)); },
    })).catch((err) => { log('readableWebSocketStream pipeTo error', err); });

    return new Response(null, { status: 101, webSocket: client });
}

async function handleTCPOutBound(remoteSocketWapper, addressRemote, portRemote, rawClientData, webSocket, vlessResponseHeader, log) {
    async function connectAndWrite(address, port) {
        const { connect } = await import("cloudflare:sockets");
        const tcpSocket = connect({ hostname: address, port: port });
        remoteSocketWapper.value = tcpSocket;
        log(`connected to ${address}:${port}`);
        const writer = tcpSocket.writable.getWriter();
        await writer.write(rawClientData);
        writer.releaseLock();
        return tcpSocket;
    }

    async function retry() {
        const tcpSocket = await connectAndWrite(proxyIP || addressRemote, portRemote)
        tcpSocket.closed.catch(error => { console.log('retry tcpSocket closed error', error); }).finally(() => { safeCloseWebSocket(webSocket); })
        remoteSocketToWS(tcpSocket, webSocket, vlessResponseHeader, null, log);
    }

    const tcpSocket = await connectAndWrite(addressRemote, portRemote);
    remoteSocketToWS(tcpSocket, webSocket, vlessResponseHeader, retry, log);
}

function makeReadableWebSocketStream(webSocketServer, earlyDataHeader, log) {
    let readableStreamCancel = false;
    const stream = new ReadableStream({
        start(controller) {
            webSocketServer.addEventListener('message', (event) => {
                if (readableStreamCancel) { return; }
                const message = event.data;
                controller.enqueue(message);
            });
            webSocketServer.addEventListener('close', () => {
                safeCloseWebSocket(webSocketServer);
                if (readableStreamCancel) { return; }
                readableStreamCancel = true;
                controller.close();
            });
            webSocketServer.addEventListener('error', (err) => {
                log('webSocketServer has error');
                controller.error(err);
            });
            const { earlyData, error } = base64ToArrayBuffer(earlyDataHeader);
            if (error) { controller.error(error); } else if (earlyData) { controller.enqueue(earlyData); }
        },
        pull(controller) {},
        cancel(reason) {
            if (readableStreamCancel) { return; }
            log(`ReadableStream was canceled, due to ${reason}`)
            readableStreamCancel = true;
            safeCloseWebSocket(webSocketServer);
        }
    });
    return stream;
}

function processVlessHeader(vlessBuffer, userID) {
    if (vlessBuffer.byteLength < 24) { return { hasError: true, message: 'invalid data' }; }
    const version = new Uint8Array(vlessBuffer.slice(0, 1));
    let isValidUser = false;
    let isUDP = false;
    if (stringify(new Uint8Array(vlessBuffer.slice(1, 17))) === userID) { isValidUser = true; }
    if (!isValidUser) { return { hasError: true, message: 'invalid user' }; }

    const optLength = new Uint8Array(vlessBuffer.slice(17, 18))[0];
    const command = new Uint8Array(vlessBuffer.slice(18 + optLength, 18 + optLength + 1))[0];

    if (command === 1) {
    } else if (command === 2) {
        isUDP = true;
    } else {
        return { hasError: true, message: `command ${command} is not support` };
    }
    const portIndex = 18 + optLength + 1;
    const portBuffer = vlessBuffer.slice(portIndex, portIndex + 2);
    const portRemote = new DataView(portBuffer).getUint16(0);

    let addressIndex = portIndex + 2;
    const addressBuffer = new Uint8Array(vlessBuffer.slice(addressIndex, addressIndex + 1));

    const addressType = addressBuffer[0];
    let addressLength = 0;
    let addressValueIndex = addressIndex + 1;
    let addressValue = '';
    switch (addressType) {
        case 1:
            addressLength = 4;
            addressValue = new Uint8Array(vlessBuffer.slice(addressValueIndex, addressValueIndex + addressLength)).join('.');
            break;
        case 2:
            addressLength = new Uint8Array(vlessBuffer.slice(addressValueIndex, addressValueIndex + 1))[0];
            addressValueIndex += 1;
            addressValue = new TextDecoder().decode(vlessBuffer.slice(addressValueIndex, addressValueIndex + addressLength));
            break;
        case 3:
            addressLength = 16;
            const dataView = new DataView(vlessBuffer.slice(addressValueIndex, addressValueIndex + addressLength));
            const ipv6 = [];
            for (let i = 0; i < 8; i++) { ipv6.push(dataView.getUint16(i * 2).toString(16)); }
            addressValue = ipv6.join(':');
            break;
        default:
            return { hasError: true, message: `invild addressType` };
    }
    if (!addressValue) { return { hasError: true, message: `addressValue is empty` }; }

    return { hasError: false, addressRemote: addressValue, addressType, portRemote, rawDataIndex: addressValueIndex + addressLength, vlessVersion: version, isUDP };
}

async function remoteSocketToWS(remoteSocket, webSocket, vlessResponseHeader, retry, log) {
    let remoteChunkCount = 0;
    let chunks = [];
    let vlessHeader = vlessResponseHeader;
    let hasIncomingData = false;
    await remoteSocket.readable.pipeTo(
        new WritableStream({
            start() {},
            async write(chunk, controller) {
                hasIncomingData = true;
                if (webSocket.readyState !== WS_READY_STATE_OPEN) {
                    controller.error('webSocket.readyState is not open');
                }
                if (vlessHeader) {
                    webSocket.send(await new Blob([vlessHeader, chunk]).arrayBuffer());
                    vlessHeader = null;
                } else {
                    webSocket.send(chunk);
                }
            },
            close() { log(`remoteConnection!.readable is close`); },
            abort(reason) { console.error(`remoteConnection!.readable abort`, reason); },
        })
    ).catch((error) => {
        console.error(`remoteSocketToWS has exception `, error.stack || error);
        safeCloseWebSocket(webSocket);
    });

    if (hasIncomingData === false && retry) {
        log(`retry`)
        retry();
    }
}

function base64ToArrayBuffer(base64Str) {
    if (!base64Str) { return { error: null }; }
    try {
        base64Str = base64Str.replace(/-/g, '+').replace(/_/g, '/');
        const decode = atob(base64Str);
        const arryBuffer = Uint8Array.from(decode, (c) => c.charCodeAt(0));
        return { earlyData: arryBuffer.buffer, error: null };
    } catch (error) { return { error }; }
}

function isValidUUID(uuid) {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidRegex.test(uuid);
}

const WS_READY_STATE_OPEN = 1;
const WS_READY_STATE_CLOSING = 2;

function safeCloseWebSocket(socket) {
    try {
        if (socket.readyState === WS_READY_STATE_OPEN || socket.readyState === WS_READY_STATE_CLOSING) {
            socket.close();
        }
    } catch (error) { console.error('safeCloseWebSocket error', error); }
}

const byteToHex = [];
for (let i = 0; i < 256; ++i) { byteToHex.push((i + 256).toString(16).slice(1)); }
function unsafeStringify(arr, offset = 0) {
    return (byteToHex[arr[offset + 0]] + byteToHex[arr[offset + 1]] + byteToHex[arr[offset + 2]] + byteToHex[arr[offset + 3]] + "-" + byteToHex[arr[offset + 4]] + byteToHex[arr[offset + 5]] + "-" + byteToHex[arr[offset + 6]] + byteToHex[arr[offset + 7]] + "-" + byteToHex[arr[offset + 8]] + byteToHex[arr[offset + 9]] + "-" + byteToHex[arr[offset + 10]] + byteToHex[arr[offset + 11]] + byteToHex[arr[offset + 12]] + byteToHex[arr[offset + 13]] + byteToHex[arr[offset + 14]] + byteToHex[arr[offset + 15]]).toLowerCase();
}
function stringify(arr, offset = 0) {
    const uuid = unsafeStringify(arr, offset);
    if (!isValidUUID(uuid)) { throw TypeError("Stringified UUID is invalid"); }
    return uuid;
}

async function handleDNSQuery(udpChunk, webSocket, log, vlessResponseHeader) {
    try {
        const dnsServer = '8.8.4.4'; 
        const dnsPort = 53;
        let vlessHeader = vlessResponseHeader;
        const { connect } = await import("cloudflare:sockets");
        const tcpSocket = connect({ hostname: dnsServer, port: dnsPort });
        log(`connected to ${dnsServer}:${dnsPort}`);
        const writer = tcpSocket.writable.getWriter();
        const lengthBuffer = new Uint8Array([udpChunk.byteLength >> 8, udpChunk.byteLength & 0xff]);
        await writer.write(await new Blob([lengthBuffer, udpChunk]).arrayBuffer());
        writer.releaseLock();

        await tcpSocket.readable.pipeTo(new WritableStream({
            async write(chunk) {
                if (webSocket.readyState === WS_READY_STATE_OPEN) {
                    const udpData = chunk.slice(2);
                    if (vlessHeader) {
                        webSocket.send(await new Blob([vlessHeader, new Uint8Array([0, udpData.byteLength >> 8, udpData.byteLength & 0xff]), udpData]).arrayBuffer());
                        vlessHeader = null;
                    } else {
                        webSocket.send(await new Blob([new Uint8Array([0, udpData.byteLength >> 8, udpData.byteLength & 0xff]), udpData]).arrayBuffer());
                    }
                }
            },
            close() { log(`dns server tcp is close`); },
            abort(reason) { console.error(`dns server tcp is abort`, reason); },
        }));
    } catch (error) { console.error(`handleDNSQuery have exception`, error.message); }
}

function getVLESSConfig(userID, hostName) {
    const vlessMain = `vless://${userID}@${hostName}:443?encryption=none&security=tls&sni=${hostName}&fp=randomized&type=ws&host=${hostName}&path=%2F%3Fed%3D2048#Cloudflare-Vless`;
    return vlessMain;
}
