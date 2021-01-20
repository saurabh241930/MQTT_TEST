from flask import Flask
from flask import request
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
import paho.mqtt.client as mqtt
from utils import connect_mqtt,publish
import random,time,os,sys


app = Flask(__name__)

fake_marble_data = [
    {"marble":"M1","angle":12,"X":100,"Y":200,"value":None,"location":"BLOCK C1"},
    {"marble":"M2","angle":22,"X":120,"Y":300,"value":None,"location":"BLOCK C1"},
    {"marble":"M3","angle":14,"X":300,"Y":600,"value":None,"location":"BLOCK C1"},
    {"marble":"M4","angle":22,"X":120,"Y":400,"value":None,"location":"BLOCK C1"}
]

fake_topic_data = [
    {"topic":"/Vehicle1/location/x/value","params":["location","X","value"]},
    {"topic":"/Vehicle1/location/y/value","params":["location","Y","value"]}
]


broker = 'broker.emqx.io'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = connect_mqtt(client_id,broker,port)
client.loop_start()

def publish_data_to_topic(topic,found_marble,vehicle_no):
    found_topic = next(t for t in fake_topic_data if t["topic"] == topic)
    data = dict()
    for p in found_topic["params"]:
        data[p] = found_marble[p]

    data["vehicle_no"] = vehicle_no

    publish(client,topic,str(data))

        



@app.route('/target/<marble_name>/<vehicle_no>', methods = ['GET'])
def test_topic(marble_name,vehicle_no):
    found_marble = next(item for item in fake_marble_data if item["marble"] == marble_name)
    publish_data_to_topic("/Vehicle1/location/x/value",found_marble,vehicle_no)
    publish_data_to_topic("/Vehicle1/location/y/value",found_marble,vehicle_no)
    
    return jsonify({"status":"Succesfully sent the data"})











if __name__ == '__main__':
    app.run()