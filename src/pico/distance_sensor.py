import busio  # type: ignore
import vl53l4cx  # type: ignore

class DistanceSensor:
    def __init__(self, i2c, address=0x29):
        self.sensor = vl53l4cx.VL53L4CX(i2c, address=address)  # if supported
        self.sensor.distance_mode = 1
        self.sensor.timing_budget = 50
        self.sensor.start_ranging()

    def get_distance(self):
        if self.sensor.data_ready:
            data = self.sensor.distance  # in cm
            self.sensor.clear_interrupt()
            # print(f"Distance sensor: {data}")
            return data
        return -1