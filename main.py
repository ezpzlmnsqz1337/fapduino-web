from microWebSrv import MicroWebSrv

import arm

robotArm = arm.Arm()
# robotArm.setData('10|20|30|40|open')

print('WS ACCEPT')
def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback


def _recvTextCallback(webSocket, msg):
    print('Rcv message: %s' % msg)
    if 'arm:setData:' in msg:
        armData = msg.split(':')[2]
        robotArm.setData(armData)
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:getData' in msg:
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:leftRightBy' in msg:
        robotArm.incrementPosition(0, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:upDownBy' in msg:
        robotArm.incrementPosition(1, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:frontBackBy' in msg:
        robotArm.incrementPosition(2, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'claw:rotateBy' in msg:
        robotArm.incrementPosition(3, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:leftRight' in msg:
        robotArm.setPosition(0, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:upDown' in msg:
        robotArm.setPosition(1, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'arm:frontBack' in msg:
        robotArm.setPosition(2, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'claw:rotate' in msg:
        robotArm.setPosition(3, msg.split(':')[2])
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'claw:open' in msg:
        robotArm.clawOpen()
        webSocket.SendText('armData:%s' % robotArm.getData())
    elif 'claw:close' in msg:
        robotArm.clawClose()
        webSocket.SendText('armData:%s' % robotArm.getData())


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
