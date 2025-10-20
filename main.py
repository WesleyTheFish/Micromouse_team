import time
import board
#import simpleio
import digitalio
import analogio
import pwmio
import busio

# Define directions
CLOCKWISE = (True, False)  # FORWARD
COUNTERCLOCKWISE = (False, True)  # BACKWARD


def motor_setup():
    # Declaring the motor pins
    # Motor Right
    motorRa = digitalio.DigitalInOut(board.GP2)
    motorRb = digitalio.DigitalInOut(board.GP3)
    motorRa.direction = digitalio.Direction.OUTPUT
    motorRb.direction = digitalio.Direction.OUTPUT

    # Motor Left
    motorLa = digitalio.DigitalInOut(board.GP4)
    motorLb = digitalio.DigitalInOut(board.GP5)
    motorLa.direction = digitalio.Direction.OUTPUT
    motorLb.direction = digitalio.Direction.OUTPUT

    # Enable pin determines power
    enb1 = pwmio.PWMOut(board.GP6)
    enb2 = pwmio.PWMOut(board.GP7)

    # Initialize duty cycle to 0
    enb1.duty_cycle = 0
    enb2.duty_cycle = 0

    # Motor rotational direction
    motorRa.value, motorRb.value = CLOCKWISE
    motorLa.value, motorLb.value = CLOCKWISE

    return [[motorRa, motorRb], [motorLa, motorLb],[enb1,enb2]]

"""
# Functions for movement
def move_forward(motors,time_seconds):
    motors[0][0].value, motors[0][1].value = CLOCKWISE
    motors[1][0].value, motors[1][1].value = CLOCKWISE

    # Set duty cycle for motors
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000

    # Sleep for specified time
    time.sleep(time_seconds)

    # Stop motors after specified time
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0

"""
def stop_motors(motors):
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0

def move_forward(motors):
    motors[0][0].value, motors[0][1].value = CLOCKWISE
    motors[1][0].value, motors[1][1].value = CLOCKWISE
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000


def move_backwards(motors,time_seconds):
    motors[0][0].value, motors[0][1].value = COUNTERCLOCKWISE
    motors[1][0].value, motors[1][1].value = COUNTERCLOCKWISE

    # Set duty cycle for motors
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000

    # Sleep for specified time
    time.sleep(time_seconds)

    # Stop motors after specified time
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0

def turn_right(motors,time_seconds):
    #set direction
    motors[0][0].value, motors[0][1].value = COUNTERCLOCKWISE
    motors[1][0].value, motors[1][1].value = CLOCKWISE

    # Set duty cycle for motors
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000

    # Sleep for specified time
    time.sleep(time_seconds)

    # Stop motors after specified time
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0

def turn_left(motors,time_seconds):
    #set direction
    motors[0][0].value, motors[0][1].value = CLOCKWISE
    motors[1][0].value, motors[1][1].value = COUNTERCLOCKWISE

    # Set duty cycle for motors
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000

    # Sleep for specified time
    time.sleep(time_seconds)
    # Stop motors after specified time
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0

def encoder_init():
    # Declare break sensor pins
    encoder = digitalio.DigitalInOut(board.GP16)
    encoder.direction = digitalio.Direction.INPUT
    encoder.pull = digitalio.Pull.DOWN

    return encoder


def main():
    #instantiate_OLED()
    #sense_distance()
    #break_sensor()
    motors = motor_setup()
    encoder = encoder_init()


    move_forward(motors)
    enum = 0
    while(True):
        time.sleep(0.01)
        print(enum)
        enum+=1
        print(encoder.value)

    move_duration = 4  # seconds
    print_interval = 0.01  # seconds

    start_time = time.monotonic()
    last_print = start_time

    # Start moving forward
    move_forward(motors)

    while True:
        now = time.monotonic()

        # Print encoder value every 0.01 seconds
        if now - last_print >= print_interval:
            print("Encoder:", encode.value)
            last_print = now

        # Stop motors after move_duration seconds
        if now - start_time >= move_duration:
            stop_motors(motors)
            break  # exit loop (or keep looping if you want)






if __name__ == "__main__":
    main()
