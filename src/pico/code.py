import time
import assembly
import asyncio

async def control():
    while True:
        mouse.move_forward(10000)
        await asyncio.sleep(2)
        mouse.stop_motors()
        await asyncio.sleep(1)
        mouse.move_forward(40000)
        await asyncio.sleep(2)
        mouse.stop_motors()
        # print("IMU gyro: " + mouse.imu.getGyroscope())
        print(f"Left encoder: {mouse.left_encoder.read()}")
        print(f"Right encoder: {mouse.right_encoder.read()}")
        # print("Distance sensor: " + mouse.distance.get_distance())
        await asyncio.sleep(1)

async def main():
    left_encoder = asyncio.create_task(mouse.left_encoder.monitor())
    right_encoder = asyncio.create_task(mouse.right_encoder.monitor())
    # give encoder tasks a moment to start and sample initial states
    await asyncio.sleep(0.01)
    primary = asyncio.create_task(control())
    await asyncio.gather(left_encoder, right_encoder, primary)

if __name__ == "__main__":
    mouse = assembly.Assembly()
    asyncio.run(main())
