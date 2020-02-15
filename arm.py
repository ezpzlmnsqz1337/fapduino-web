import myservo

servoBasePin = 5
servoLeftPin = 18
servoRightPin = 19
servoGripPin = 21
servoGripRotatePin = 22

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


class Arm:
    def __init__(self):
        self.servoBase = myservo.MyServo(
            servoBasePin, servoBaseLow, servoBaseHigh, servoBasePosition)
        self.servoLeft = myservo.MyServo(
            servoLeftPin, servoLeftLow, servoLeftHigh, servoLeftPosition)
        self.servoRight = myservo.MyServo(
            servoRightPin, servoRightLow, servoRightHigh, servoRightPosition)
        self.servoGripRotate = myservo.MyServo(
            servoGripRotatePin, servoGripRotateLow, servoGripRotateHigh, servoGripRotatePosition)
        self.servoGrip = myservo.MyServo(
            servoGripPin, servoGripLow, servoGripHigh, servoGripPosition)

    def getData(self):
        data = [self.servoBase.getPosition(), self.servoLeft.getPosition(), self.servoRight.getPosition(), self.servoGripRotate.getPosition(), self.servoGrip.getPosition()]
        return '|'.join(str(d) for d in data)

    def setData(self, data):
        print('set data1 %s' % data)
        positions = data.split('|')
        if len(positions) != 5:
            return
        self.servoBase.moveTo(int(positions[0]))
        self.servoLeft.moveTo(int(positions[1]))
        self.servoRight.moveTo(int(positions[2]))
        self.servoGripRotate.moveTo(int(positions[3]))
        print('set data2 %s' % positions)

        if positions[4] == 'open':
            self.servoGrip.moveTo(servoGripLow)
        elif positions[4] == 'close':
            self.servoGrip.moveTo(servoGripHigh)

    def setPosition(self, servo, position):
        armData = self.getData().split('|')
        armData[servo] = str(position)
        self.setData('|'.join(armData))

    def incrementPosition(self, servo, value):
        armData = self.getData().split('|')
        armData[servo] = str(int(armData[servo]) + int(value))
        self.setData('|'.join(armData))

    def clawOpen(self):
        armData = self.getData().split('|')
        armData[4] = 'open'
        self.setData('|'.join(armData))

    def clawClose(self):
        armData = self.getData().split('|')
        armData[4] = 'close'
        self.setData('|'.join(armData))
