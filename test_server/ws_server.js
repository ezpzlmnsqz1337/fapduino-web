const WebSocket = require('ws')

const wss = new WebSocket.Server({ port: 8085 })
console.log('Server is listenning on port: 8085')

armData = [ 0, 0, 0, 0, 'open']

wss.on('connection', ws => {
    // send initial configuration

    ws.on('message', message => {
        console.log('message: ', message)
        if (message.includes('arm:leftRight')) {
            armData[0] = parseInt(message.substring(message.lastIndexOf(':') + 1))
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        } else if (message.includes('arm:upDown')) {
            armData[1] = parseInt(message.substring(message.lastIndexOf(':') + 1))
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        } else if (message.includes('arm:frontBack')) {
            armData[2] = parseInt(message.substring(message.lastIndexOf(':') + 1))
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        } else if (message.includes('claw:rotate')) {
            armData[3] = parseInt(message.substring(message.lastIndexOf(':') + 1))
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        } else if (message.includes('claw:open')) {
            armData[4] = message.substring(message.lastIndexOf(':') + 1)
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        } else if (message.includes('claw:close')) {
            armData[4] = message.substring(message.lastIndexOf(':') + 1)
            wss.clients.forEach(client => {
                client.send('armData:' + armData.join('|'))
            })
        }
    })

    // setInterval(() => ws.send('armData:90|150|160|30|closed'), 2000)
})