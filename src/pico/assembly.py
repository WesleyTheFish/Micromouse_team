import board # type: ignore
import digitalio
import motor
import encoder
import imu
import distance_sensor
import busio
import bitbangio

# Define directions
CLOCKWISE = (True, False)  # FORWARD
COUNTERCLOCKWISE = (False, True)  # BACKWARD
DEFAULT_POWER = 7000
# 65000

class Assembly:
    def __init__(self):
        # Motors
        self.motor_right = motor.Motor(board.GP10, board.GP9, board.GP12)
        self.motor_left = motor.Motor(board.GP22, board.GP11, board.GP8)

        # Encoders
        # self.right_encoder = encoder.Encoder(board.GP18, board.GP17)
        # self.left_encoder = encoder.Encoder(board.GP12, board.GP3)
         

        # IMU 
        imu_i2c   = busio.I2C(scl=board.GP27, sda=board.GP26)   # I2C1 hardware
        self.imu = imu.IMU(imu_i2c)  # I2C1 hardware

        # # Distance Sensor
        front_i2c = busio.I2C(scl=board.GP5,  sda=board.GP4)    # I2C0 hardware
        left_i2c  = bitbangio.I2C(scl=board.GP3,  sda=board.GP2)   # software
        right_i2c = bitbangio.I2C(scl=board.GP17, sda=board.GP16)  # software

        self.front_distance = distance_sensor.DistanceSensor(front_i2c, address=0x29)
        self.left_distance  = distance_sensor.DistanceSensor(left_i2c, address=0x29)
        self.right_distance = distance_sensor.DistanceSensor(right_i2c, address=0x29)



    def move_forward(self, speed=DEFAULT_POWER):
        self.motor_right.move_forward(CLOCKWISE, speed+350)
        self.motor_left.move_forward(COUNTERCLOCKWISE, speed)

    def move_backward(self, speed=DEFAULT_POWER):
        self.motor_right.move_backward(COUNTERCLOCKWISE, speed)
        self.motor_left.move_backward(COUNTERCLOCKWISE, speed)

    def stop_motors(self):
        self.motor_right.stop()
        self.motor_left.stop()

    def turn_right(self, speed=DEFAULT_POWER):
        self.motor_right.move_backward(COUNTERCLOCKWISE, speed)
        self.motor_left.move_forward(CLOCKWISE, speed)

    def turn_left(self, speed=DEFAULT_POWER):
        self.motor_right.move_forward(CLOCKWISE, speed)
        self.motor_left.move_backward(COUNTERCLOCKWISE, speed)