import board # type: ignore
import digitalio
import motor
import encoder
import imu
import distance_sensor
import busio
import bitbangio
import time

# Define directions

DEFAULT_POWER = 7000

TURN_KP = 200      # duty cycle per degree of error
TURN_KI = 0        # leave at 0 until kp/kd are tuned
TURN_KD = 30       # damps overshoot
TURN_MAX = 15000   # max turn duty cycle (of 65535)
TURN_MIN = 10000    # min duty cycle that still gets the wheels moving
TURN_TOLERANCE = 1 # degrees
# 65000

class Assembly:
    def __init__(self):
        # Motors
        self.motor_right = motor.Motor("right",board.GP10, board.GP9, board.GP12)
        self.motor_left = motor.Motor("left", board.GP22, board.GP11, board.GP8)

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

        self.heading = self.imu.getEuler()[0]  # Get the initial heading from the IMU



    def move_forward(self, speed=DEFAULT_POWER):
        self.motor_right.move_forward(speed+350)
        self.motor_left.move_forward(speed)

    def stop_motors(self):
        self.motor_right.stop()
        self.motor_left.stop()

    # def turn(self, angle, speed=(DEFAULT_POWER)):
    #     current_heading = self.imu.getEuler()[0]
    #     target_heading = (current_heading + angle) % 360
    #     self.motor_right.move_backward(speed)
    #     self.motor_left.move_forward(speed)

    #     while abs((target_heading - current_heading + 180) % 360 - 180) > 5:
    #         current_heading = self.imu.getEuler()[0]
    #         time.sleep(0.01)

    #     # Stop the motors
    #     print(f"Turned {angle} degrees. Current heading: {current_heading}")
    #     self.stop_motors()

    #     self.heading = current_heading  # Keep software state synchronized with the IMU


   


    def turn(self, angle, timeout=4.0):
        """Turn `angle` degrees (positive = clockwise) using a PID loop on IMU heading."""

        def wrap(a):
            # Shortest signed difference, in [-180, 180)
            return (a + 180) % 360 - 180

        def read_heading():
            # BNO055 occasionally returns None; retry briefly
            for _ in range(5):
                euler = self.imu.getEuler()
                if euler is not None and euler[0] is not None:
                    return euler[0]
            return None

        heading = read_heading()
        if heading is None:
            print("IMU read failed, aborting turn")
            return

        target = (heading + angle) % 360
        integral = 0.0
        prev_error = wrap(target - heading)
        prev_time = time.monotonic()
        start_time = prev_time
        settled = 0

        while True:
            now = time.monotonic()
            dt = now - prev_time
            if dt <= 0:
                continue

            heading = read_heading()
            if heading is None:
                continue

            error = wrap(target - heading)

            # Finished once we've held within tolerance for a few consecutive reads
            if abs(error) <= TURN_TOLERANCE:
                self.stop_motors()
                settled += 1
                if settled >= 3:
                    break
                prev_error, prev_time = error, now
                continue
            settled = 0

            if now - start_time > timeout:
                print("Turn timed out")
                break

            # PID
            integral += error * dt
            integral = max(-150, min(150, integral))  # anti-windup
            derivative = (error - prev_error) / dt
            output = TURN_KP * error + TURN_KI * integral + TURN_KD * derivative

            # Clamp, with a minimum so the motors overcome friction
            power = min(TURN_MAX, max(TURN_MIN, abs(output)))
            power = int(power)

            if output > 0:   # clockwise: right wheel back, left wheel forward
                self.motor_right.move_backward(power)
                self.motor_left.move_forward(power)
            else:            # counter-clockwise
                self.motor_right.move_forward(power)
                self.motor_left.move_backward(power)

            prev_error, prev_time = error, now
            time.sleep(0.005)

        self.stop_motors()
        print(f"Turned {angle} degrees. Final heading: {heading}, error: {error}")
        self.heading = heading


        
