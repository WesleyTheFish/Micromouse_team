import asyncio
import digitalio # type: ignore

class Encoder:
    def __init__(self, pin1, pin2):
        self.encoder1 = self.pin_init(pin1)
        self.encoder2 = self.pin_init(pin2)
        self.counter = 0
        asyncio.run(self)

    def pin_init(self, pin):
            # Declare break sensor pins
            encoder = digitalio.DigitalInOut(pin)
            encoder.direction = digitalio.Direction.INPUT
            encoder.pull = digitalio.Pull.DOWN
            return encoder

    def read(self):
        return self.counter
    
    async def monitor(self):
        self.last_value1 = self.encoder1.value
        self.last_value2 = self.encoder2.value
        while True:
            current_value1 = self.encoder1.value
            current_value2 = self.encoder2.value
            if current_value1 and current_value2:
                if not self.last_value1:
                    counter += 1
                if not self.last_value2:
                    counter -= 1
            self.last_value1 = current_value1
            self.last_value2 = current_value2
            await asyncio.sleep(0.001)