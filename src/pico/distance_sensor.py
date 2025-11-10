#Time of flight
import adafruit_vl53l1x # type: ignore
import board # type: ignore
import busio # type: ignore
import time

def sense_distance():

    #i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    i2c = busio.I2C(sda=board.GP14,scl=board.GP15)

    sensor = adafruit_vl53l1x.VL53L1X(i2c)

    # OPTIONAL: can set non-default values
    sensor.distance_mode = 1
    sensor.timing_budget = 100


    print("VL53L1X Simple Test.")
    print("--------------------")
    model_id, module_type, mask_rev = sensor.model_info
    print("Model ID: 0x{:0X}".format(model_id))
    print("Module Type: 0x{:0X}".format(module_type))
    print("Mask Revision: 0x{:0X}".format(mask_rev))
    print("Distance Mode: ", end="")
    if sensor.distance_mode == 1:
        print("SHORT")
    elif sensor.distance_mode == 2:
        print("LONG")
    else:
        print("UNKNOWN")
    print("Timing Budget: {}".format(sensor.timing_budget))
    print("--------------------")

    sensor.start_ranging()



    while True:
        if sensor.data_ready:
            print("Distance: {} cm".format(sensor.distance))
            sensor.clear_interrupt()
            time.sleep(1.0)




    """
    # OPTIONAL: can set non-default values
    sensor.start_ranging()

    print("Here")

    while True:
        if sensor.data_ready:
            print("Distance: {} cm".format(sensor.distance))
            sensor.clear_interrupt()
            time.sleep(1.0)
    """

