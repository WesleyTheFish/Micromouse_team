import digitalio
import board

class Encoder:
    def __init__(self, port):
        self.encoder = digitalio.DigitalInOut(port)
        self.encoder.direction = digitalio.Direction.INPUT
        self.encoder.pull = digitalio.Pull.DOWN

    def read(self):
        return self.encoder.value
    

   

    