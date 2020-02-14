from microWebSrv import MicroWebSrv

import arm

robotArm = arm.Arm()


def _acceptWebSocketCallback(webSocket, httpClient):
    print('WS ACCEPT')
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback


def _recvTextCallback(webSocket, msg):
    if 'arm:setData:' in msg:
        armData = msg.split(':')[2]
        robotArm.setData(armData)
        webSocket.SendText('armData:%s' % armData)
    elif 'arm:getData' in msg:
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:leftRight' in msg:
        robotArm.setPosition(0, msg.split(':')[2])
        webSocket.SendText('armData:%s' % armData)
    elif 'arm:frontBack' in msg:
        robotArm.setPosition(1, msg.split(':')[2])
        webSocket.SendText('armData:%s' % armData)
    elif 'arm:upDown' in msg:
        robotArm.setPosition(2, msg.split(':')[2])
        webSocket.SendText('armData:%s' % armData)
    elif 'claw:rotate' in msg:
        robotArm.setPosition(3, msg.split(':')[2])
        webSocket.SendText('armData:%s' % armData)
    elif 'claw:open' in msg:
        robotArm.clawOpen()
        webSocket.SendText('armData:%s' % armData)
    elif 'claw:close' in msg:
        robotArm.clawClose()
        webSocket.SendText('armData:%s' % armData)


def _recvBinaryCallback(webSocket, data):
    print('WS RECV DATA : %s' % data)


def _closedCallback(webSocket):
    print('WS CLOSED')


# ----------------------------------------------------------------------------

# routeHandlers = [
#	( '/test',	'GET',	_httpHandlerTestGet ),
#	( '/test',	'POST',	_httpHandlerTestPost )
# ]


srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen = 256
srv.WebSocketThreaded = True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()

# ----------------------------------------------------------------------------
