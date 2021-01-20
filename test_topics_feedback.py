import paho.mqtt.client as mqtt
from utils import connect_mqtt,subscribe
import random,time,os,sys



broker = 'broker.emqx.io'
port = 1883
topic = [("/Vehicle1/location/x/value",0),("/Vehicle1/location/y/value",1)]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public

def run():
    client = connect_mqtt(client_id,broker,port)
    subscribe(client,topic)
    client.loop_forever()


if __name__ == '__main__':
    run()