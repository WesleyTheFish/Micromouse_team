import busio  # type: ignore
import vl53l4cx  # type: ignore

class DistanceSensor:
    def __init__(self, sda, scl):
        i2c = busio.I2C(sda=sda, scl=scl)
        self.sensor = vl53l4cx.VL53L4CX(i2c)
        self.sensor.distance_mode = 1   # 1 = short, 2 = long
        self.sensor.timing_budget = 50
        self.sensor.start_ranging()

    def get_distance(self):
        if self.sensor.data_ready:
            data = self.sensor.distance  # in cm
            self.sensor.clear_interrupt()
            print(f"Distance sensor: {data}")
            return data
        return -1