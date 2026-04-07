import board # type: ignore
import digitalio
import motor
import encoder
import imu
import distance_sensor

# Define directions
CLOCKWISE = (True, False)  # FORWARD
COUNTERCLOCKWISE = (False, True)  # BACKWARD
DEFAULT_POWER = 65000

class Assembly:
    def __init__(self):
        # Motors
        self.motor_right = motor.Motor(board.GP16, board.GP17, board.GP18)
        self.motor_left = motor.Motor(board.GP15, board.GP14, board.GP13)

        # Encoders
        self.right_encoder = encoder.Encoder(board.GP8, board.GP19)
        self.left_encoder = encoder.Encoder(board.GP12, board.GP3)

        # IMU
        # self.imu = imu.IMU(board.GP4, board.GP5)

        # Distance Sensor
        # self.distance = distance_sensor.DistanceSensor(board.GP10, board.GP11)



    def move_forward(self, speed=DEFAULT_POWER):
        self.motor_right.move_forward(CLOCKWISE, speed)
        self.motor_left.move_forward(CLOCKWISE, speed)

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