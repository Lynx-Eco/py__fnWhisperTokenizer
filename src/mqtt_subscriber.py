import paho.mqtt.client as mqtt

# Global variable to keep track of the number of messages received
line_number = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("whisper/inference-text")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global line_number
    line_number += 1
    message = msg.payload.decode('utf-8')
    print(f"Line {line_number}: {message}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()