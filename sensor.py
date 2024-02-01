from machine import Pin, SoftI2C
import bme280 as bme280
from time import sleep
# from bme280 import BME280, BME280_OSAMPLE_16, BME280_OSAMPLE_8

i2c0 = SoftI2C(sda=Pin(8), scl=Pin(9))
i2c1 = SoftI2C(sda=Pin(6), scl=Pin(7))

temp_offset = [0, 0]
pressure_offset = [0, 0]
rh_offset = [-0, -2]


def read_values(bme):
    """ human readable values """

    t, p, h = bme.read_compensated_data()

    p = p / 256

    h = h / 1024
    
    return (t / 100, p/100, h)


def read_sensor(bme0_address = 0x77, bme1_address = 0x77, mode = bme280.BME280_OSAMPLE_16):
    try:
        
        bme0 = bme280.BME280(i2c=i2c0, address=bme0_address, mode=mode)
        bme1 = bme280.BME280(i2c=i2c1, address=bme1_address, mode=mode)
        print("=======================")
        print(f"Sensor 0: {bme0.values}")
        print(f"Sensor 1: {bme1.values}")
        
        values0 = read_values(bme0)
        values1 = read_values(bme1)
        
        offset_values0 = (values0[0]+temp_offset[0], values0[1]+pressure_offset[0], values0[2]+rh_offset[0])
        offset_values1 = (values1[0]+temp_offset[1], values1[1]+pressure_offset[1], values1[2]+rh_offset[1])
        
        return [offset_values0, offset_values1]
    
    except Exception as e:
        print(f"{e}")
        # raise e
    
    return []

if __name__ == "__main__":
    while True:
        print(read_sensor())
        sleep(1)

    pass