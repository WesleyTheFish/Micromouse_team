import time
import assembly
import digitalio
import microcontroller
import board


def print_side_distances(mouse):
    measurements = []

    left_distance = mouse.left_distance.get_distance()
    if left_distance != -1:
        measurements.append(f"Left: {left_distance} cm")

    right_distance = mouse.right_distance.get_distance()
    if right_distance != -1:
        measurements.append(f"Right: {right_distance} cm")

    if measurements:
        print(" | ".join(measurements))


if __name__ == "__main__":
    mouse = assembly.Assembly()

    # button setup
    button = digitalio.DigitalInOut(board.GP6)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP



    mouse.turn(90)

    while True:
        # print_side_distances(mouse)
        # time.sleep(0.05)

        if button.value:
            print("Button pressed, resetting...")
            mouse.stop_motors()
            time.sleep(1)
            microcontroller.reset()


        
        # mouse.move_forward()
        
        # if(distance_front < 15 and distance_front != -1):
        #     mouse.stop_motors()
        #     print("stopped")
        #     time.sleep(1)
        #     break
