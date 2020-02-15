class Pin:
    def __init__(self, number):
        self.number = number

class PWM:
    def __init__(self, pin, freq, duty):
        self.pin = pin
        self.freq = freq
        self.du = duty

    def duty(self, duty):
        self.du = duty
        print('Setting duty: %i' % duty)

