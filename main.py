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
    motorRa.value = True
    motorRb.value = False
    motorLa.value = True
    motorLb.value = False


    motorRa.value, motorRb.value = CLOCKWISE
    motorLa.value, motorLb.value = COUNTERCLOCKWISE
    # Set duty cycle for motors
    enb1.duty_cycle = 65000
    enb2.duty_cycle = 65000
    # Sleep for specified time
    time.sleep(5)
    # Stop motors after specified time
    enb1.duty_cycle = 0
    enb2.duty_cycle = 0

    return [[motorRa, motorRb], [motorLa, motorLb],[enb1,enb2]]

# Functions for movement
def move_forward(motors,time_seconds):
    motors[0][0].value, motors[0][1].value = CLOCKWISE
    motors[1][0].value, motors[1][1].value = COUNTERCLOCKWISE
    # motorRa.value, motorRb.value = CLOCKWISE
    # motorLa.value, motorLb.value = CLOCKWISE
    # Set duty cycle for motors
    motors[2][0].duty_cycle = 65000
    motors[2][1].duty_cycle = 65000
    #enb1.duty_cycle = 65000
    #enb2.duty_cycle = 65000
    # Sleep for specified time
    time.sleep(time_seconds)
    # Stop motors after specified time
    motors[2][0].duty_cycle = 0
    motors[2][1].duty_cycle = 0
    #enb1.duty_cycle = 0
    #enb2.duty_cycle = 0
    print("hello")

def move_backwards(time_seconds):
    motorRa.value, motorRb.value = COUNTERCLOCKWISE
    motorLa.value, motorLb.value = COUNTERCLOCKWISE
    # Set duty cycle for motors
    enb1.duty_cycle = 65000
    enb2.duty_cycle = 65000
    # Sleep for specified time
    time.sleep(time_seconds)
    # Stop motors after specified time
    enb1.duty_cycle = 0
    enb2.duty_cycle = 0

def turn_right(time_seconds):
    motorRa.value, motorRb.value = CLOCKWISE
    motorLa.value, motorLb.value = COUNTERCLOCKWISE
    # Set duty cycle for motors
    enb1.duty_cycle = 65000
    enb2.duty_cycle = 65000
    # Sleep for specified time
    time.sleep(time_seconds)
    # Stop motors after specified time
    enb1.duty_cycle = 0
    enb2.duty_cycle = 0

def turn_left(time_seconds):
    motorRa.value, motorRb.value = COUNTERCLOCKWISE
    motorLa.value, motorLb.value = CLOCKWISE
    # Set duty cycle for motors
    enb1.duty_cycle = 65000
    enb2.duty_cycle = 65000
    # Sleep for specified time
    time.sleep(time_seconds)
    # Stop motors after specified time
    enb1.duty_cycle = 0
    enb2.duty_cycle = 0

def encoder():
    # Declare encoder pins
    encoder1 = digitalio.DigitalInOut(board.GP27)
    encoder1.direction = digitalio.Direction.OUTPUT

    encoder2 = digitalio.DigitalInOut(board.GP26)
    encoder2.direction = digitalio.Direction.OUTPUT

    while True:
        print(encoder1.value, encoder2.value)
        time.sleep(0.01)

def main():
    #instantiate_OLED()
    #sense_distance()
    #break_sensor()
    motors = motor_setup()


    # move_forward(motors,5)





if __name__ == "__main__":
    main()
