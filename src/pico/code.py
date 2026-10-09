import time
import assembly
import asyncio
import digitalio
import microcontroller
import board

async def control():
    while True:
        pass
        # mouse.move_forward(10000)
        # await asyncio.sleep(20)
        # mouse.stop_motors()
        # await asyncio.sleep(1)
        # mouse.move_forward(40000)
        # await asyncio.sleep(2)
        # mouse.stop_motors()
        # # print("IMU gyro: " + mouse.imu.getGyroscope())
        # # print(f"Left encoder: {mouse.left_encoder.read()}")
        # # print(f"Right encoder: {mouse.right_encoder.read()}")
        # # print("Distance sensor: " + mouse.distance.get_distance())
        # await asyncio.sleep(1)

# async def main():
#     left_encoder = asyncio.create_task(mouse.left_encoder.monitor())
#     right_encoder = asyncio.create_task(mouse.right_encoder.monitor())
#     # give encoder tasks a moment to start and sample initial states
#     await asyncio.sleep(0.01)
#     primary = asyncio.create_task(control())
#     await asyncio.gather(left_encoder, right_encoder, primary)

if __name__ == "__main__":
    mouse = assembly.Assembly()

    # button setup
    button = digitalio.DigitalInOut(board.GP6)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    while True:
        if button.value:
            print("Button pressed, resetting...")
            mouse.stop_motors()
            time.sleep(1)
            # microcontroller.reset()

        # gyro_x, gyro_y, gyro_z = mouse.imu.getEuler()
        # print(f"IMU euler: X={gyro_x:.2f}")


        print(f"Right distance: {mouse.right_distance.get_distance()}")
        # print("test")
        
        
        # if(distance_front < 5 and distance_front != -1):
        #     # mouse.stop_motors()
        #     print("stopped")
        #     break
    
        # mouse.left_distance.get_distance()
        # mouse.front_distance.get_distance()
        # mouse.right_encoder.monitor2()

    # while True:
    #     distance = mouse.distance.get_distance()
    #     print(f"Distance sensor: {distance}")
    #     time.sleep(0.5)S


    # asyncio.run(main())
