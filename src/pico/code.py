import time
import assembly
import digitalio
import microcontroller
import board


if __name__ == "__main__":
    mouse = assembly.Assembly()

    # button setup
    button = digitalio.DigitalInOut(board.GP6)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP



    mouse.turn(90)

    while True:

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
