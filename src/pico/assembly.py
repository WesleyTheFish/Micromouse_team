import board # type: ignore
import motor
import encoder
import imu
import distance_sensor

# Define directions
CLOCKWISE = (True, False)  # FORWARD
COUNTERCLOCKWISE = (False, True)  # BACKWARD

class Assembly:
    def __init__(self):
        # Motors
        self.motor_right = motor.Motor(board.GP2, board.GP3, board.GP6)
        self.motor_left = motor.Motor(board.GP4, board.GP5, board.GP7)

        # Encoders
        self.right_encoder = encoder.Encoder(board.GP18)
        self.left_encoder = encoder.Encoder(board.GP16)

        # IMU
        self.imu = imu.IMU()

        # Distance Sensor
        self.distance = distance_sensor.DistanceSensor(board.GP12, board.GP13)



    def move_forward(self):
        self.motor_right.move_forward(CLOCKWISE)
        self.motor_left.move_forward(CLOCKWISE)

    def move_backward(self):
        self.motor_right.move_backward(COUNTERCLOCKWISE)
        self.motor_left.move_backward(COUNTERCLOCKWISE)

    def stop_motors(self):
        self.motor_right.stop()
        self.motor_left.stop()

    def turn_right(self):
        self.motor_right.move_backward(COUNTERCLOCKWISE)
        self.motor_left.move_forward(CLOCKWISE)

    def turn_left(self):
        self.motor_right.move_forward(CLOCKWISE)
        self.motor_left.move_backward(COUNTERCLOCKWISE)