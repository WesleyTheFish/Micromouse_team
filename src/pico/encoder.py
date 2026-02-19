import asyncio
import digitalio

class Encoder:
    def __init__(self, pin1, pin2):
        self.encoder1 = self.pin_init(pin1)
        self.encoder2 = self.pin_init(pin2)
        self.counter = 0
        self.last_state = (self.encoder1.value, self.encoder2.value)

    def pin_init(self, pin):
        encoder = digitalio.DigitalInOut(pin)
        encoder.direction = digitalio.Direction.INPUT
        encoder.pull = digitalio.Pull.DOWN
        return encoder

    def read(self):
        return self.counter

    async def monitor(self):
        while True:
            current_state = (self.encoder1.value, self.encoder2.value)

            if current_state != self.last_state:
                # Simple quadrature direction detection
                if self.last_state == (0, 0):
                    if current_state == (1, 0):
                        self.counter += 1
                    elif current_state == (0, 1):
                        self.counter -= 1

                self.last_state = current_state

            await asyncio.sleep(0.001)