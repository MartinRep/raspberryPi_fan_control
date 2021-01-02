import paho.mqtt.client as mqtt 
import json


class mqttConn:
    
    def __init__(self, 
                    callback,
                    broker="domovsk",
                    port=1883,
                    username="username",
                    password="password",
                    topic="displaypi"):
        self.mqttBroker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password 
        self.callback = callback
        self.client = mqtt.Client(self.topic, clean_session=False)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect=self.on_connect
        self.client.connect(self.mqttBroker)
        
    def on_connect(self, mqttc, obj, flags, rc):
        self.client.subscribe(self.topic)
        self.client.on_message=self.on_message
        print("Client Subsicribed")
    
    def subscribe(self):
        self.client.loop_forever(retry_first_connection=False)

    def unsubscribe(self):
        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        print("received message: " + str(message.payload.decode("utf-8")))
        self.callback(json.loads(message.payload.decode("utf-8")))

    def publish(self, msg):
        self.client.publish(self.topic, json.dumps(msg))
        print(f"just published message: {msg} to the topic {self.topic}")
