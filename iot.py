import mqtt_client
import wifi
from ucollections import namedtuple
import time

SensorMeasure = namedtuple("SensorMeasure", ("name", "value"))

# SensorMeasures = list[SensorMeasure]

SENSOR_TYPE = "bme280"
SYSTEM_TYPE = "pico_humidity"


def event_template(sensor_type, sensor_id, system_id, sensor_ts, metric_name, metric_value): 
    return {
        "sensor_id": sensor_id,
        "sensor_type": sensor_type, 
        "system_id": system_id,
        "metric_name": metric_name,
        "metric_value": metric_value,
        "timestamp": sensor_ts
    }


def create_message(channel, sensor_id, measure, value):
    
    # tz1 = timezone(timedelta(hours=-8))
        
    system_id = f"{SYSTEM_TYPE}_{sensor_id:03}"
    
    tz_hours = -8
    tz_offset = -8 * 60 * 60
    now = time.gmtime(time.time() + tz_offset)
    
    timeformat = f"{now[0]:04}-{now[1]:02}-{now[2]:02} {now[3]:02}:{now[4]:02}:{now[5]:02}{tz_hours:03}:00"
    return event_template(SENSOR_TYPE, f"{SENSOR_TYPE}_{channel}", system_id, timeformat, measure, value)


def send(channel:int, system_id:int, measures:list, mqtt = None):

        
    messages = [create_message(channel, system_id, name, value) for name, value in measures]
                            
    for message in messages:                    
        print(f"message: {message}")
        mqtt_client.send_message(mqtt, mqtt_client.MQTT_TOPIC, message)
