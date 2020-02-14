import machine
import time
import pyb


class MyServo:
    def __init__(self, servoPin, minimum, maximum, position):
        self.servoPin = machine.Pin(servoPin, machine.Pin.OUT)
        self.minimum = machine.Pin(minimum, machine.Pin.OUT)
        self.maximum = machine.Pin(maximum, machine.Pin.OUT)
        self.position = machine.Pin(position, machine.Pin.OUT)
        self.servo = pyb.Servo(self.servoPin)

        self.servo.angle(self.position)

    def moveBy(self, value):
        newValue = min(self.maximum, max(self.minimum, self.position + value))
        servo.angle(newValue)
        self.position = newValue

    def moveTo(self, value):
        if self.position == value:
            return

        newValue = min(self.maximum, max(self.minimum, self.position + value))
        increment = 1 if newValue > self.position else -1
        while self.position != newValue:
            self.moveBy(newValue)
            time.sleep(15)

    def getPosition(self):
        return self.position
