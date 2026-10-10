from maze import Maze
from wall import Wall
from cell import Cell

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

#! Constants for mouse movement and wall following
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


#! PID Constants for turning
TURN_KP = 200      # duty cycle per degree of error
TURN_KI = 0        # leave at 0 until kp/kd are tuned
TURN_KD = 30       # damps overshoot
TURN_MAX = 15000   # max turn duty cycle (of 65535)
TURN_MIN = 10000    # min duty cycle that still gets the wheels moving
TURN_TOLERANCE = 1 # degrees
# 65000



class Mouse:
    def __init__(self, start, finish, size=5):
        self.start:list = [start]
        self.position = start
        self.dirct_facing = "north"
        self.finish:list = finish
        self.maze = Maze(finish, size=size,key=False)
        self.size = size

        #! Hardware!!
        # Distance Sensor
        front_i2c = busio.I2C(scl=board.GP5,  sda=board.GP4)    # I2C0 hardware
        left_i2c  = bitbangio.I2C(scl=board.GP3,  sda=board.GP2)   # software
        right_i2c = bitbangio.I2C(scl=board.GP17, sda=board.GP16)  # software

        self.front_distance = distance_sensor.DistanceSensor(front_i2c, address=0x29)
        self.left_distance  = distance_sensor.DistanceSensor(left_i2c, address=0x29)
        self.right_distance = distance_sensor.DistanceSensor(right_i2c, address=0x29)

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
        self.heading = self.imu.getEuler()[0]  # Get the initial heading from the IMU


    
    def solve_maze(self):
        """through trial and error the mouse explores the maze and returns the shortest path to the finish"""
        path_there = []
        path_back = []

        print("solving maze")

        # runs through the maze twice, once to the finish and once back to the start
        for destination in (self.finish, self.start):

            # changes maze's finish to the start for the return trip
            if destination == self.start:
                self.maze.finish = self.start

            while self.position not in destination:

                # update surrounding wall status
                self.update_walls()
                print("walls updated")

                # update weights of all cells
                self.maze.wipe_weights()
                
                # updates weights of cells(method starts at each finishing square)
                for cord in destination:
                    self.maze.update_weights(self.maze.cells[cord],None)

                # self.maze.print_maze(self.position)

                # move mouse to next best Cell
                direction = self.find_next_move()
                self.next_step(direction)

                # logs the path the mouse took
                if destination == self.finish:
                    path_there.append(self.position)
                else:
                    path_back.append(self.position)

                time.sleep(1)  # slow down for debugging

        self.smooth_path(path_there)
        self.smooth_path(path_back)

        # returns the shortest path
        if len(path_back) < len(path_there):
            path_back.reverse()
            return path_back
        else:
            return path_there
    
    def smooth_path(self, path):
        """removes any unnecessary turns in the path"""
        branches = []

        # index out of bounds if the last element is a duplicate(issue should never happen)
        for cord in range(1,len(path),1):
            for check in range(cord):
                if path[cord] == path[check] and path[cord+1] != path[check-1]:
                    branches.append((check, cord))

        branches.reverse()

        for branch in branches:
            first,last = branch
            for _ in range(first, last, 1):
                path.remove(path[first])

    #done maybe
    def update_walls(self):
        """mouse looks around and updates it's maze with the wall data surrounding it"""
        # sets value of wall in maze equal to the counterpart in the maze_key
        cur_cell = self.maze.cells[self.position]
        # key_cell = self.maze_key.cells[self.position]

        if self.dirct_facing == "north":
            cur_cell.bottom.update_wall(False)
            cur_cell.right.update_wall(self.right_distance.is_blocked())
            cur_cell.top.update_wall(self.front_distance.is_blocked())
            cur_cell.left.update_wall(self.left_distance.is_blocked())
        elif self.dirct_facing == "south":
            cur_cell.top.update_wall(False)
            cur_cell.left.update_wall(self.right_distance.is_blocked())
            cur_cell.bottom.update_wall(self.front_distance.is_blocked())
            cur_cell.right.update_wall(self.left_distance.is_blocked())
        elif self.dirct_facing == "east":
            cur_cell.left.update_wall(False)
            cur_cell.top.update_wall(self.left_distance.is_blocked())
            cur_cell.right.update_wall(self.front_distance.is_blocked())
            cur_cell.bottom.update_wall(self.right_distance.is_blocked())
        elif self.dirct_facing == "west":
            cur_cell.right.update_wall(False)
            cur_cell.bottom.update_wall(self.left_distance.is_blocked())
            cur_cell.left.update_wall(self.front_distance.is_blocked())
            cur_cell.top.update_wall(self.right_distance.is_blocked())

    def find_next_move(self):
        """takes current position and returns the direction you need to go to get to the next Cell of smallest weight"""
        next_cell = None
        least_num_moves = self.size**2+1

        # list of all surrounding cells possible to get to 
        possible_cells = []
        cell,y = self.position
        if not self.maze.cells[self.position].left.is_blocked: possible_cells.append(self.maze.cells[cell-1,y])
        if not self.maze.cells[self.position].right.is_blocked: possible_cells.append(self.maze.cells[cell+1,y])
        if not self.maze.cells[self.position].top.is_blocked: possible_cells.append(self.maze.cells[cell,y-1])
        if not self.maze.cells[self.position].bottom.is_blocked: possible_cells.append(self.maze.cells[cell,y+1])

        """This is where optimization could happen balancing number of turns to distance traveled"""
        for cell in possible_cells:
            if cell.weight == least_num_moves:
                if self.dirct_facing == self.direct_to_cell(cell):
                    next_cell = cell
                    least_num_moves = cell.weight
            elif cell.weight < least_num_moves:
                least_num_moves = cell.weight
                next_cell = cell

        return self.direct_to_cell(next_cell)
    
    def next_step(self, direction):

        if direction == "north":
            heading = 0
        elif direction == "east":
            heading = 90
        elif direction == "south":
            heading = 180
        elif direction == "west":
            heading = 270


        # turns the mouse to face the direction it needs to go
        self.turn_to_heading(heading)

        # moves the mouse forward 18cm (1 cell) in the direction it is facing
        self.move_forward_distance(18)

        # moves the mouse in internal representation of the maze to the next cell
        self.dirct_facing = direction
        if direction == "north":
            self.position = (self.position[0], self.position[1]-1)
        elif direction == "south":
            self.position = (self.position[0], self.position[1]+1)
        elif direction == "east":
            self.position = (self.position[0]+1, self.position[1])
        elif direction == "west":
            self.position = (self.position[0]-1, self.position[1])
        
        # throws error if mouse moves out of bounds of the maze
        if 0 > self.position[0] or self.position[0] > self.maze.size-1 or 0 > self.position[1] or self.position[1] > self.maze.size-1:
            raise ValueError("Mouse has moved out of bounds")
              
    def direct_to_cell(self,destination:Cell):
        """given a desired cell to travel to, returns the direction you would need to travel in to get to it"""
        x,y = destination.address
        a,b = self.position
        
        # cells aligned on y-axis
        if a == x:
            if b > y:
                return "north"
            else:
                return "south"
        else:
            if a > x:
                return "west"
            else:
                return "east"

    def _read_heading(self):
        for _ in range(5):
            euler = self.imu.getEuler()
            if euler is not None and euler[0] is not None:
                return euler[0]
        return None
    
    def move_forward_distance(self, distance_cm, timeout=10.0):
        """Drive forward distance_mm while holding self.heading and tracking the right wall."""
        distance_mm = distance_cm * 10.0
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
        
    def turn_to_heading(self, target_heading, timeout=4.0):
        """Turn to an absolute IMU heading (0-360) using a PID loop.
        Takes the shortest direction: positive error = clockwise."""

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

        target = target_heading % 360   # accepts -90, 450, etc.

        heading = read_heading()
        if heading is None:
            print("IMU read failed, aborting turn")
            return

        error = wrap(target - heading)
        integral = 0.0
        prev_error = error
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

            power = int(min(TURN_MAX, max(TURN_MIN, abs(output))))

            if output > 0:   # clockwise: right wheel back, left wheel forward
                self.motor_right.move_backward(power)
                self.motor_left.move_forward(power)
            else:            # counter-clockwise
                self.motor_right.move_forward(power)
                self.motor_left.move_backward(power)

            prev_error, prev_time = error, now
            time.sleep(0.005)

        self.stop_motors()
        print(f"Target {target}. Final heading: {heading}, error: {error}")
        self.heading = heading
        