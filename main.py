import sensor
import iot
import wifi
import mqtt_client
from time import sleep
import ujson

MEASURE_TEMP = "temperature"
MEASURE_PRESSURE = "pressure"
MEASURE_HUMIDITY = "humidity"

bme0_address = 0x77
bme1_address = 0x77
system_id = 0
poll_interval_seconds = 30

def get_ssid():
    with open('secrets.json') as fp:
        secrets = ujson.loads(fp.read())    
        
    ssid = secrets["wifi"]["ssid"]
    pwd = secrets["wifi"]["password"]
    
    return ssid, pwd

def get_mqtt_config():
    with open('secrets.json') as fp:
        secrets = ujson.loads(fp.read())    
        
    broker = secrets["mqtt"]["broker"]
    
    return broker


def create_measure(temperature, pressure, humidity):
    return [
        (MEASURE_TEMP, temperature),
        (MEASURE_PRESSURE, pressure),
        (MEASURE_HUMIDITY, humidity),
    ]    

def run():

    wlan_client = None
    mqtt = None
    
    first = True
    while True:
        try:
            if not (wlan_client and wlan_client.active() and wlan_client.isconnected()):
                
                print("getting ssid")
                ssid, pwd = get_ssid()
                print("connecting to wifi")
                wlan_client = wifi.connect(ssid, pwd)
                mqtt_broker = get_mqtt_config()
                print(f"connecting to mqtt {mqtt_broker}")
                mqtt = mqtt_client.setup(mqtt_broker)
        
            print("getting sensor readings")
            sensor_reading = sensor.read_sensor(
                bme0_address=bme0_address,
                bme1_address=bme1_address
                )
            
            print(f"sensors {sensor_reading}")
            
            if not first:
            
                for channel, (temperature, pressure, humidity) in enumerate(sensor_reading):
                    measures = create_measure(temperature, pressure, humidity)    
                    iot.send(channel, system_id, measures, mqtt)

            else:
                print("skipping first reading")
                first = False
            
            disconnect(wlan_client, mqtt)
            sleep(poll_interval_seconds)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            disconnect(wlan_client, mqtt)
            wlan_client = None
            mqtt = None
            sleep(5)
        

def disconnect(wlan_client, mqtt):
    try:
        if mqtt:
            mqtt.disconnect()
        if wlan_client:
            wifi.disconnect(wlan_client)
    except Exception as e:
        print(f"error: {e}")
    
if __name__ == "__main__":
    print("running")
    run()
