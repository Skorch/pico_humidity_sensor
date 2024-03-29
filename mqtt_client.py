# module imports
import machine
import ssl
import ubinascii
import json
import lib.ntptime as ntptime

from lib.simple import MQTTClient
# import mip



# def install():
#     mip.install("https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.simple/umqtt/simple.py")
#     # mip.install("https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/datetime/datetime.py")


# Wi-Fi network constants

# MQTT client and broker constants
MQTT_CLIENT_KEY = "./certs/SensorHub_4541DDAA20550D40566163953AA78D9C-private.pem.key"
MQTT_CLIENT_CERT = "./certs/SensorHub_4541DDAA20550D40566163953AA78D9C-certificate.pem.crt"
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC="iot/sensible/sensor"

MQTT_BROKER_CA = "./certs/aws.rc" #"AmazonRootCA1.pem"


# create MQTT client that use TLS/SSL for a secure connection
mqtt_ping_timer = None


# function that reads PEM file and return byte array of data
def read_pem(file):
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])

        return ubinascii.a2b_base64(base64_text)

# read the data in the private key, public certificate, and
# root CA files
key = read_pem(MQTT_CLIENT_KEY)
cert = read_pem(MQTT_CLIENT_CERT)
ca = read_pem(MQTT_BROKER_CA)


# callback function to handle received MQTT messages
def on_mqtt_msg(topic, msg):
    # convert topic and message from bytes to string
    topic_str = topic.decode()
    msg_str = msg.decode()

    print(f"RX: {topic_str}\n\t{msg_str}")



# callback function to periodically send MQTT ping messages
# to the MQTT broker
# def send_mqtt_ping(t):
#     print("TX: ping")
#     mqtt_client.ping()


def send_message(mqtt_target, mqtt_topic, values):

    print(f"sending sensor reading '{values}'...")

    message = {"message" : values}
    # await asyncio.wrap_future(mqtt_target.publish(topic=mqtt_topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE))
    result =  mqtt_target.publish(topic=mqtt_topic, msg=json.dumps(message), qos=1)
    print(f"result: {result}")
    print("Update request published.")




def setup(mqtt_broker):
    global mqtt_ping_timer

    mqtt_client = MQTTClient(
        MQTT_CLIENT_ID,
        mqtt_broker,
        keepalive=60,
        ssl=True,
        ssl_params={
            "key": key,
            "cert": cert,
            "server_hostname": mqtt_broker,
            "cert_reqs": ssl.CERT_REQUIRED,
            "cadata": ca,
        },
    )
    

    # update the current time on the board using NTP
    ntptime.settime()

    # install()

    print(f"Connecting to MQTT broker: {mqtt_broker}")

    # register callback to for MQTT messages, connect to broker and
    # subscribe to LED topic
    mqtt_client.set_callback(on_mqtt_msg)
    mqtt_client.connect()

    print(f"Connected to MQTT broker: {mqtt_broker}")

    # turn on-board LED on
    # led.off()

    # create timer for periodic MQTT ping messages for keep-alive
    # mqtt_ping_timer = Timer(
    #     mode=Timer.PERIODIC, period=mqtt_client.keepalive * 1000, callback=send_mqtt_ping
    # )
    
    return mqtt_client
    
