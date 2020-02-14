from microWebSrv import MicroWebSrv
import machine
import dht

import servo

servoBasePin = 6
servoLeftPin = 7
servoRightPin = 8
servoGripPin = 9
servoGripRotatePin = 10

servoBasePosition = 90
servoBaseLow = 0
servoBaseHigh = 180

servoLeftPosition = 30
servoLeftLow = 20
servoLeftHigh = 100

servoRightPosition = 100
servoRightLow = 90
servoRightHigh = 160

servoGripPosition = 95
servoGripLow = 0
servoGripHigh = 180

servoGripRotatePosition = 90
servoGripRotateLow = 0
servoGripRotateHigh = 180

servoBase = servo.MyServo(servoBasePin, servoBaseLow, servoBaseHigh, servoBasePosition)
servoLeft = servo.MyServo(servoLeftPin, servoLeftLow, servoLeftHigh, servoLeftPosition)
servoRight = servo.MyServo(servoRightPin, servoRightLow, servoRightHigh, servoRightPosition)
servoGrip = servo.MyServo(servoGripPin, servoGripLow, servoGripHigh, servoGripPosition)
servoGripRotate = servo.MyServo(servoGripRotatePin, servoGripRotateLow, servoGripRotateHigh, servoGripRotatePosition)

# ----------------------------------------------------------------------------

@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
				<head>
					<meta charset="UTF-8" />
						<title>TEST GET</title>
				</head>
				<body>
						<h1>TEST GET</h1>
						Client IP address = %s
						<br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
				</body>
		</html>
	""" % httpClient.GetIPAddr()
	httpResponse.WriteResponseOk( headers		 = None,
									contentType	 = "text/html",
									contentCharset = "UTF-8",
									content 		 = content )


@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestPostedFormData()
	firstname = formData["firstname"]
	lastname  = formData["lastname"]
	content   = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
						<title>TEST POST</title>
				</head>
				<body>
						<h1>TEST POST</h1>
						Firstname = %s<br />
						Lastname = %s<br />
				</body>
		</html>
	""" % ( MicroWebSrv.HTMLEscape(firstname),
				MicroWebSrv.HTMLEscape(lastname) )
	httpResponse.WriteResponseOk( headers		 = None,
									contentType	 = "text/html",
									contentCharset = "UTF-8",
									content 		 = content )


@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
				<head>
					<meta charset="UTF-8" />
						<title>TEST EDIT</title>
				</head>
				<body>
	"""
	content += "<h1>EDIT item with {} variable arguments</h1>"\
		.format(len(args))

	if 'index' in args :
		content += "<p>index = {}</p>".format(args['index'])

	if 'foo' in args :
		content += "<p>foo = {}</p>".format(args['foo'])

	content += """
				</body>
		</html>
	"""
	httpResponse.WriteResponseOk( headers		 = None,
									contentType	 = "text/html",
									contentCharset = "UTF-8",
									content 		 = content )

# ----------------------------------------------------------------------------


def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def measureTemperatureCallback(webSocket):
	d.measure()
	webSocket.SendText("TEMP IS:%s" % d.temperature())
	webSocket.SendText("HUMIDITY IS:%s" % d.humidity())

def measureDistanceCallback(webSocket):
	distance = sensor.distance_cm()
	webSocket.SendText("DISTANCE IS:%s" % distance)

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	if 'SET STATE:' in msg:
		newState = msg.split(':')[1]
		# set led to given state
		led(int(newState))
		# send WS info about the new state
		webSocket.SendText("STATE IS:%s" % newState)
	elif 'GET STATE' in msg:
		# send WS info about the new state
		webSocket.SendText("STATE IS:%s" % led.value())
	elif 'GET TEMP' in msg:
		# send WS info about the new state
		d.measure()
		webSocket.SendText("TEMP IS:%s" % d.temperature())
		webSocket.SendText("HUMIDITY IS:%s" % d.humidity())
	elif 'SUBSCRIBE TEMP' in msg:
		# send WS info about the new state
		timTemp.init(period=2500, mode=machine.Timer.PERIODIC, callback=lambda t:measureTemperatureCallback(webSocket))
		print('TEMP init')
	elif 'SUBSCRIBE DISTANCE' in msg:
		# send WS info about the new state
		print('Timer init')
		timDistance.init(period=500, mode=machine.Timer.PERIODIC, callback=lambda t:measureDistanceCallback(webSocket))
	elif 'GET DISTANCE' in msg:
		# send WS info about the distance
		distance = sensor.distance_cm()
		webSocket.SendText("DISTANCE IS:%s" % distance)
	elif 'ROTATE ANGLE CW' in msg:
		angle = int(msg.split(':')[2])
		index = int(msg.split(':')[1])
		motors[index].rotateCWAngle(angle)
		webSocket.SendText("STEPPER ROTATING:%s°" % angle)
	elif 'ROTATE ANGLE CCW' in msg:
		angle = int(msg.split(':')[2])
		index = int(msg.split(':')[1])
		motors[index].rotateCCWAngle(angle)
		webSocket.SendText("STEPPER ROTATING:%s°" % angle)
	elif 'ROTATE STEPS CW' in msg:
		steps = int(msg.split(':')[2])
		index = int(msg.split(':')[1])
		motor = motors[index]
		motor.setTargetPosition(motor.getPosition() + steps)
		webSocket.SendText("STEPPER ROTATING:%s steps" % steps)
	elif 'ROTATE STEPS CCW' in msg:
		steps =int( msg.split(':')[2])
		index = int(msg.split(':')[1])
		motor = motors[index]
		motor.setTargetPosition(motor.getPosition() - steps)
		webSocket.SendText("STEPPER ROTATING:%s steps" % steps)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")
	timTemp.deinit()
	timDistance.deinit()

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()

# ----------------------------------------------------------------------------
