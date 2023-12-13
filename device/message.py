from paho.mqtt import client as mqtt_client
import json

class Message:
    def __init__(self, on_received):
        client = mqtt_client.Client("iot-epd-signage")
        client.on_connect = self.on_connect
        client.connect('beam.soracom.io', 1883)
        client.loop_start()
        self.client = client
        self.on_received = on_received
        
    def wait(self):
        self.client.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.publish('iot-epd-signage/started', json.dumps({"hello": "world!"}))
            client.subscribe('iot-epd-signage/schedules')
            client.on_message = self.on_message
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.on_received(json.loads(msg.payload.decode()))

