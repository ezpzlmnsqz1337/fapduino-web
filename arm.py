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


class Arm:
    def __init__(self):
        self.servoBase = servo.MyServo(
            servoBasePin, servoBaseLow, servoBaseHigh, servoBasePosition)
        self.servoLeft = servo.MyServo(
            servoLeftPin, servoLeftLow, servoLeftHigh, servoLeftPosition)
        self.servoRight = servo.MyServo(
            servoRightPin, servoRightLow, servoRightHigh, servoRightPosition)
        self.servoGrip = servo.MyServo(
            servoGripPin, servoGripLow, servoGripHigh, servoGripPosition)
        self.servoGripRotate = servo.MyServo(
            servoGripRotatePin, servoGripRotateLow, servoGripRotateHigh, servoGripRotatePosition)

    def getData(self):
        clawState = 'open' if self.servoGripRotate.getPosition(
        ) == self.servoGripRotate.getPosition() else 'closed'

        return self.servoBase.getPosition() + '|' + self.servoLeft.getPosition() + '|'
        + self.servoRight.getPosition() + '|' + self.servoGrip.getPosition() + '|'
        + clawState

    def setData(self, data):
        positions = data.split('|')
        if len(positions) != 4:
            return
        self.servoBase.setPosition(int(positions[0]))
        self.servoLeft.setPosition(int(positions[1]))
        self.servoRight.setPosition(int(positions[2]))
        self.servoGripRotate.setPosition(int(positions[3]))

        if positions[4] == 'open':
            self.clawOpen()
        elif positions[4] == 'close':
            self.clawClose()

    def setPosition(self, servo, position):
        armData = self.getData()
        armData.split('|')[servo] = position
        self.setData('|'.join(armData))

    def clawOpen(self):
        armData = self.getData()
        armData.split('|')[servo] = servoGripHigh
        self.setData('|'.join(armData))

    def clawClose(self):
        armData = self.getData()
        armData.split('|')[servo] = servoGripLow
        self.setData('|'.join(armData))
