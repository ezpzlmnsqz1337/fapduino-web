const WebSocket = require('ws')

const wss = new WebSocket.Server({ port: 8085 })
console.log('Server is listenning on port: 8085')

wss.on('connection', ws => {
    // send initial configuration

    ws.on('message', message => {
        console.log('message: ', message)
    })
})