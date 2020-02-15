import servo
import time
import machine

class MyServo:
    def __init__(self, servoPin, minimum, maximum, position):
        self.servoPin = machine.Pin(servoPin)
        self.minimum = minimum
        self.maximum = maximum
        self.position = position
        self.servo = servo.Servo(self.servoPin, freq = 50)

        self.servo.writeAngle(self.position)

    def moveTo(self, value):
        print('value %s' % value)
        newValue = min(self.maximum, max(self.minimum, value))
        print('new value %s' % newValue)
        self.servo.writeAngle(newValue)
        self.position = newValue

    def moveBy(self, value):
        if self.position == value:
            return

        newValue = min(self.maximum, max(self.minimum, self.position + value))
        increment = 1 if newValue > self.position else -1
        while self.position != newValue:
            self.moveTo(self.position + increment)
            time.sleep(15)

    def getPosition(self):
        return self.position
