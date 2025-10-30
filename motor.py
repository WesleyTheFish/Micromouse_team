import digitalio
import pwmio


class Motor:
    def __init__(self, port_a, port_b, enable_pin):
        self.motor_a = digitalio.DigitalInOut(port_a)
        self.motor_a.direction = digitalio.Direction.OUTPUT

        self.motor_b = digitalio.DigitalInOut(port_b)
        self.motor_b.direction = digitalio.Direction.OUTPUT

        self.enable_pin = pwmio.PWMOut(enable_pin)

        # Initialize duty cycle to 0
        self.enable_pin.duty_cycle = 0

    def move_forward(self, dir, speed=65000, ):
        self.motor_a.value, self.motor_b.value = dir
        self.enable_pin.duty_cycle = speed

    def move_backward(self, dir, speed=65000):
        self.motor_a.value, self.motor_b.value = dir
        self.enable_pin.duty_cycle = speed

    def stop(self):
        self.enable_pin.duty_cycle = 0

