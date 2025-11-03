import board



def imu_setputest():
    '''initialize and test IMU'''
    print("here")
    try:
        i2c = board.I2C()
        sensor = adafruit_bno055.BNO055_I2C(i2c)
        return sensor
    except (RunTimeError, ValueError) as error:
        print("IMU Error")
    print("IMU successfully running")