import network
import socket
from time import sleep
# from picozero import pico_temp_sensor, pico_led
import machine
# import mip
import ujson


led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)

max_connect_seconds = 30

def connect(ssid, password):
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    print("activating wlan...")
    wlan.active(True)
    print("connecting to wlan...")
    wlan.connect(ssid, password)
    print(f'Waiting for connection... {wlan.status()}')
    connect_seconds = 0
    while wlan.isconnected() == False:
        
        led.toggle()
        print(f'({connect_seconds}s) Waiting for connection... {wlan.status()}')
        sleep(1)
        connect_seconds +=1
        
        if connect_seconds >= max_connect_seconds:
            raise Exception(f"Failed to get wlan connection after {connect_seconds} seconds.")

    led.on()
    # ip = wlan.ifconfig()[0]
    # print(f'Connected on {ip}')
    return wlan

def disconnect(wlan):
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()
    wlan=None    

# wlan = connect()
# install()
# setup_mqtt()

# try:
#     ip = connect()
#     install()
#     setup_mqtt()



# except KeyboardInterrupt:
#     machine.reset()

