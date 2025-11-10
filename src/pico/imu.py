import board # type: ignore
import adafruit_bno055 # type: ignore


class IMU:    
    def __init__(self):
        try:
            i2c = board.I2C()
            sensor = adafruit_bno055.BNO055_I2C(i2c)
            return sensor
        except (RuntimeError, ValueError) as error:
            print("IMU Error")
        print("IMU successfully running")

    def getTemperature(self):
        return self.sensor.temperature

    def getAcceleration(self):
        return self.sensor.linear_acceleration

    def getGyroscope(self):
        return self.sensor.gyro

    def getMagnetometer(self):
        return self.sensor.magnetic
    
    def getEuler(self):
        return self.sensor.euler
    
    def getQuaternion(self):
        return self.sensor.quaternion
    
    def getGravity(self):
        return self.sensor.gravity
    
    def getLinearAcceleration(self):
        return self.sensor.linear_acceleration
