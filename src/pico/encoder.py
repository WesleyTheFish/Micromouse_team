import asyncio
import digitalio
import rotaryio
import time

class Encoder:
    def __init__(self, pin1, pin2):
        self.encoder = rotaryio.IncrementalEncoder(pin1, pin2)
        # self.encoder1 = self.pin_init(pin1)
        # self.encoder2 = self.pin_init(pin2)
        # self.counter = 0
        # self.last_state = (self.encoder1.value, self.encoder2.value)

    def pin_init(self, pin):
        encoder = digitalio.DigitalInOut(pin)
        encoder.direction = digitalio.Direction.INPUT
        encoder.pull = digitalio.Pull.DOWN
        return encoder

    def read(self):
        return self.counter


    def monitor2(self):
        last_position = None

        while True:
            # Read the current position (this is an integer that goes up or down)
            current_position = self.encoder.position
            print(f"Encoder Position: {current_position}")
            
            # Only print when the position actually changes
            if last_position is None or current_position != last_position:
                print(f"Encoder Position: {current_position}")
                last_position = current_position
                
            # A small delay keeps the loop from spamming the serial console too fast
            time.sleep(0.01)

    def monitor(self):
        while True:
            current_state = (self.encoder1.value, self.encoder2.value)
            print(f"Encoder state: {current_state}, Counter: {self.counter}")
            if current_state != self.last_state:
                # Simple quadrature direction detection
                if self.last_state == (0, 0):
                    if current_state == (1, 0):
                        self.counter += 1
                    elif current_state == (0, 1):
                        self.counter -= 1

                self.last_state = current_state

            # await asyncio.sleep(0.001)s