import threading
import queue
from typing import List
import paho.mqtt.client as mqtt

import sys
sys.path.append('./src')
from driver import driver

MQTT_BROKER_PORT = 1883
MQTT_BROKER_ADDRESS = "127.0.0.1"
MQTT_SUBSCRIBE_TOPIC = "whisper/inference-text"

# Queue for storing messages
message_queue = queue.Queue()

# MQTT message callback
def on_message(client, userdata, message):
    message_queue.put(message.payload)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)
client.subscribe(MQTT_SUBSCRIBE_TOPIC)
client.loop_start()

# tokenizer `driver` setup
driverInst = driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100)

# Worker thread function
def process_messages():
    while True:
        # Retrieve message from queue
        message = message_queue.get()
        # Process message
        # (Your processing logic here)
        # print(message)
        
        # step the driver with message
        newTokens: List[str]
        ctxBuffer: List[List[str]]
        committed_tokens: List[str]
        newTokens, ctxBuffer, committed_tokens = driverInst.drive(message.decode('utf-8'))
        
        print(newTokens)
        
        message_queue.task_done()

# Starting the worker thread
worker_thread = threading.Thread(target=process_messages)
worker_thread.start()

# Rest of your code
