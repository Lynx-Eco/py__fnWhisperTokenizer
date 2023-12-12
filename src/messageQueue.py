import datetime
import socket
import threading
import queue
from typing import List
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


import sys
sys.path.append('./src')
from driver import driver

import time

WAIT_TIME = 16
print("Sleeping for " + str(WAIT_TIME) + " seconds to ensure the broker container is ready.")
time.sleep(WAIT_TIME) # Give a healthy amount of time to allow `emqx/emqx` broker to fully hydrate.
print("LeeeeeEEEEERRRRoooooyyyYYYYYY JJJJJEeeennnnnNNNkkkKKins!!!!!")

MQTT_BROKER_PORT = 1883
MQTT_BROKER_ADDRESS = "emqx"
MQTT_SUBSCRIBE_TOPIC = "whisper/inference-text"

MQTT_BROKER_ADDRESS = "127.0.0.1"
MQTT_SUBSCRIBE_TOPIC = "whisper/transcription/#"

# Queue for storing messages
message_queue = queue.Queue()

# MQTT message callback
def on_message(client, userdata, mqtt_message):
    message_queue.put(mqtt_message)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)
client.subscribe(MQTT_SUBSCRIBE_TOPIC)
client.loop_start()

# tokenizer `driver` setup
# Dictionary to store driver instances by topic
driver_instances = {}
driverInst = driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100)

# Worker thread function
def process_messages():
    while True:
        # Retrieve message from queue
        mqtt_message = message_queue.get()
        str_msg = mqtt_message.payload.decode('utf-8')
        
        topic = mqtt_message.topic.split('/')[2]
        
        # Check if a driver instance exists for the current topic, if not, create one
        if topic not in driver_instances:
            driver_instances[topic] = driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100)
        
        # Use the topic-specific driver instance to process the message
        driverInst = driver_instances[topic]
        newTokens, ctxBuffer, committed_tokens = driverInst.drive(str_msg)
                
        if (len(newTokens)):
            # annotatedPublishMsg = <<isodate>> <<cpu hostname>> newTokens
            # emit `newTokens` to `whisper/confirmedTokens` here.
            # Format the current datetime as ISO 8601 and get the hostname
            now_iso = datetime.datetime.now().isoformat()
            # hostname = socket.gethostname()
            hostname = topic
            # Construct the annotated publish message
            annotatedPublishMsg = f"{now_iso} {hostname} {newTokens}"
            publish.single("whisper/confirmedTokens/" + hostname, annotatedPublishMsg, hostname=MQTT_BROKER_ADDRESS)
            annotatedPublishMsgStr = f"{now_iso} {hostname} {' '.join(newTokens)}"
            publish.single("whisper/aggregateTokens", annotatedPublishMsgStr, hostname=MQTT_BROKER_ADDRESS)
            
            print(annotatedPublishMsg)
        
        message_queue.task_done()

# Starting the worker thread
worker_thread = threading.Thread(target=process_messages)
worker_thread.start()

# Rest of your code
