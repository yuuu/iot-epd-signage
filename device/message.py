from paho.mqtt import client as mqtt_client

class Message:
    def __init__(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client("iot-epd-signage")
        client.on_connect = on_connect
        client.connect('beam.soracom.io', 1883)
        client.loop_start()
        self.client = client
        
    def publish(self):
        print('publish')
        self.client.publish('iot-epd-signage', '{"hello": "world!"}')

    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe('#')
        print('subscribe')
        self.client.on_message = on_message
        self.client.loop_forever()
        
