import time
import assembly


def main():
    mouse = assembly.Assembly()

    while True:
        mouse.move_forward()
        time.sleep(2)
        mouse.stop_motors()
        time.sleep(1)
        mouse.move_backward()
        time.sleep(2)
        mouse.stop_motors()
        print("IMU gyro: " + mouse.imu.getGyroscope())
        print("Left encoder: " + mouse.left_encoder.read())
        print("Right encoder: " + mouse.right_encoder.read())
        print("Distance sensor: " + mouse.distance.get_distance())
        time.sleep(1)


if __name__ == "__main__":
    main()
