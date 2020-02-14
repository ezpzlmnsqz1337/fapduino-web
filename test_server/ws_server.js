const WebSocket = require('ws')

const wss = new WebSocket.Server({ port: 8085 })
console.log('Server is listenning on port: 8085')

wss.on('connection', ws => {
    // send initial configuration

    ws.on('message', message => {
        console.log('message: ', message)
        if(message.includes('arm:leftRight')) {
            wss.clients.forEach(client => {
                if (client.readyState === WebSocket.OPEN) {
                    console.log('armData:' + message.substring(message.lastIndexOf(':')+1).split('|')[0] + '|150|160|30|closed')
                    client.send('armData:' + message.substring(message.lastIndexOf(':')+1).split('|')[0] + '|150|160|30|closed')
                }
            })
        }
    })

    // setInterval(() => ws.send('armData:90|150|160|30|closed'), 2000)
})