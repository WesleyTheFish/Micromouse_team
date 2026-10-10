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

    button = digitalio.DigitalInOut(board.GP6)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    mouse.move_forward_distance(300)
    