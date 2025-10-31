import time
import assembly


def main():
    mouse = assembly.Assembly()


    mouse.move_forward()
    time.sleep(2)
    mouse.stop_motors()
    time.sleep(1)
    mouse.move_backward()
    time.sleep(2)
    mouse.stop_motors()



if __name__ == "__main__":
    main()
