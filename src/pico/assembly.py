import board # type: ignore
import digitalio
import motor
import encoder
import imu
import distance_sensor
import busio
import bitbangio
import time
import math

# Wheel Diameter(mm)
WHEEL_DIAMETER = 34

DEFAULT_POWER = 7000
#! PID Constants for turning
TURN_KP = 200      # duty cycle per degree of error
TURN_KI = 0        # leave at 0 until kp/kd are tuned
TURN_KD = 30       # damps overshoot
TURN_MAX = 15000   # max turn duty cycle (of 65535)
TURN_MIN = 10000    # min duty cycle that still gets the wheels moving
TURN_TOLERANCE = 1 # degrees
# 65000

#! PI constants for encoder setpoint
SPIN_KP = 15           # duty cycle per encoder count of error
SPIN_KD = 3            # duty cycle per (count/sec) of speed, this is the "brake" term
SPIN_MAX = 20000       # max duty cycle
SPIN_MIN = 7000        # min duty cycle that still moves the wheel
SPIN_TOLERANCE = 5     # counts


# --- Drive geometry (FILL THESE IN) ---
WHEEL_DIAMETER_MM = 32.0     # measure yours
COUNTS_PER_WHEEL_REV = 1400  # from your spin_counts measurement
MM_PER_COUNT = (math.pi * WHEEL_DIAMETER_MM) / COUNTS_PER_WHEEL_REV

# --- Distance loop ---
DRIVE_KP = 100          # duty cycle per mm remaining
DRIVE_MAX = 10000
DRIVE_MIN = 6500        # lowest duty that keeps both wheels moving
DRIVE_TOLERANCE_MM = 2

# --- Heading loop (output = left/right power difference) ---
HEAD_KP = 200           # duty per degree of error
HEAD_KD = 10
STEER_MAX = 4000

# --- Wall loop (output = heading offset in degrees) ---
WALL_TARGET_CM = 5.9
WALL_KP = 3.0           # degrees per cm of error
WALL_MAX_OFFSET = 10    # degrees
WALL_MAX_VALID_CM = 15  # beyond this, assume no wall (opening) and ignore it

class Assembly:
    def __init__(self):
        # Motors
        self.motor_right = motor.Motor("right",board.GP10, board.GP9, board.GP12)
        self.motor_left = motor.Motor("left", board.GP22, board.GP11, board.GP8)

        # Encoders
        # 910 counts per rev
        self.right_encoder = encoder.Encoder(board.GP15, board.GP14)
        self.left_encoder = encoder.Encoder(board.GP0, board.GP1)

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

    def spin_counts(self, counts, speed=DEFAULT_POWER, timeout=10.0):
        """Spin the right wheel until the right encoder moves `counts` ticks.
        Positive = forward, negative = backward. Returns the actual counts moved."""
        self.right_encoder.reset()
        start = time.monotonic()
        target = abs(counts)

        if counts >= 0:
            self.motor_right.move_forward(speed)
        else:
            self.motor_right.move_backward(speed)

        while abs(self.right_encoder.position) < target:
            if time.monotonic() - start > timeout:
                print("spin_counts timed out")
                break

        self.motor_right.stop()
        time.sleep(0.5)  # let the wheel coast to a halt
        final = self.right_encoder.position
        print(f"Target: {counts}, actual after coasting: {final}")
        return final

    def spin_counts_pid(self, counts, timeout=5.0):
        """Spin the right wheel to `counts` encoder ticks from the start using PD control.
        Positive = forward. Returns the final encoder position."""
        enc = self.right_encoder
        enc.reset()

        prev_pos = 0
        prev_time = time.monotonic()
        start = prev_time
        settled = 0

        while True:
            time.sleep(0.005)
            now = time.monotonic()
            dt = now - prev_time
            if dt <= 0:
                continue

            pos = enc.position
            velocity = (pos - prev_pos) / dt   # counts per second
            error = counts - pos
            prev_pos, prev_time = pos, now

            if now - start > timeout:
                print("spin_counts_pid timed out")
                break

            # Done once we've sat inside tolerance for ~50 ms
            if abs(error) <= SPIN_TOLERANCE:
                self.motor_right.stop()
                settled += 1
                if settled >= 10:
                    break
                continue
            settled = 0

            # PD on error, with the derivative taken on measured velocity
            output = SPIN_KP * error - SPIN_KD * velocity
            power = int(min(SPIN_MAX, max(SPIN_MIN, abs(output))))

            if output > 0:
                self.motor_right.move_forward(power)
            else:
                self.motor_right.move_backward(power)

        self.motor_right.stop()
        time.sleep(0.3)
        final = enc.position
        print(f"Target: {counts}, final: {final}, error: {counts - final}")
        return final

    def _read_heading(self):
        for _ in range(5):
            euler = self.imu.getEuler()
            if euler is not None and euler[0] is not None:
                return euler[0]
        return None

    def move_forward_distance(self, distance_mm, timeout=10.0):
        """Drive forward distance_mm while holding self.heading and tracking the right wall."""

        def wrap(a):
            return (a + 180) % 360 - 180

        def clamp(x, lo, hi):
            return max(lo, min(hi, x))

        enc = self.right_encoder
        enc.reset()
        target_heading = self.heading
        target_counts = distance_mm / MM_PER_COUNT

        last_wall_cm = None
        prev_err = None
        prev_time = time.monotonic()
        start = prev_time
        pos = 0

        while True:
            now = time.monotonic()
            dt = now - prev_time
            if dt <= 0:
                continue

            if now - start > timeout:
                print("move_forward_distance timed out")
                break

            # Distance loop
            pos = enc.position
            remaining_mm = (target_counts - pos) * MM_PER_COUNT
            if remaining_mm <= DRIVE_TOLERANCE_MM:
                break
            base = clamp(DRIVE_KP * remaining_mm, DRIVE_MIN, DRIVE_MAX)

            # Wall loop: right sensor only (-1 means "no new reading", so reuse the last one)
            d = self.right_distance.get_distance()
            if d != -1:
                last_wall_cm = d
            if last_wall_cm is not None and last_wall_cm < WALL_MAX_VALID_CM:
                wall_err = last_wall_cm - WALL_TARGET_CM   # + means too far from the right wall
                offset = clamp(WALL_KP * wall_err, -WALL_MAX_OFFSET, WALL_MAX_OFFSET)
            else:
                offset = 0

            # Heading loop
            heading = self._read_heading()
            if heading is None:
                continue
            err = wrap(target_heading + offset - heading)   # + means need to turn clockwise
            deriv = 0 if prev_err is None else (err - prev_err) / dt
            steer = clamp(HEAD_KP * err + HEAD_KD * deriv, -STEER_MAX, STEER_MAX)
            prev_err, prev_time = err, now

            # Clockwise = left wheel faster, right wheel slower
            left_power = int(clamp(base + steer, 0, 65535))
            right_power = int(clamp(base - steer, 0, 65535))
            self.motor_left.move_forward(left_power)
            self.motor_right.move_forward(right_power)

            time.sleep(0.005)

        self.stop_motors()
        print(f"Drove {pos * MM_PER_COUNT:.1f} mm of {distance_mm} mm")
        
