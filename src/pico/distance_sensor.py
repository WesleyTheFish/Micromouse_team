import adafruit_vl53l1x
import busio

class DistanceSensor:
    def __init__(self, sda, slc):
        i2c = busio.I2C(sda=sda, scl=slc)
        self.sensor = adafruit_vl53l1x.VL53L1X(i2c)
        self.sensor.start_ranging()

    def get_distance(self):
        if self.sensor.data_ready:
            data = self.sensor.distance
            self.sensor.clear_interrupt()
            return data
        else:
            return -1