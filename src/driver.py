import collections
from typing import List

from localConsensusByN import localConsensusByN
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime
from overlapIndex import overlapIndex


def driverStep(line: str, buffer: List[str], committed: List[str]) -> (List[str], List[str]):

    # print(line.strip())
    buffer.append(line.strip().replace('"', '').replace('\'', '').split(' '))
    
    prompt = []
    if len(committed_tokens) > PROMPT_LEN:
        prompt = committed_tokens[-PROMPT_LEN:]
    else:
        prompt = committed_tokens
    
    # this one liner filters buffer down to candidateBuffer
    candidateBuffer = [transcription[overlapIndex(prompt, transcription):] for transcription in buffer]
    
    newTokens = localConsensusByN(candidateBuffer, LOCAL_AGREEMENT_N)
    
    if len(newTokens):
        # emit `newTokens` to `whisper/confirmedTokens` here.
        # Format the current datetime as ISO 8601
        now_iso = datetime.datetime.now().isoformat()
        # Convert `newTokens` to a string and publish the message
        message = f"{now_iso} {newTokens}"
        publish.single("whisper/confirmedTokens", message, hostname="localhost")
    
    
    committed_tokens.extend(newTokens)
    
    # at the end of each loop .. we have a new committed string..

# the top level driver.  Keeps track of a minimum of state.


# committed tokens so far.
committed_tokens = []

# Global variable to keep track of the number of messages received
line_number = 0

def driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100):

    # stateful vars
    
    # the number of lines we consider at a time for LocalAgreement.
    buffer = collections.deque(maxlen=BUFFER_LEN)
    for i in range(BUFFER_LEN):
        buffer.append([])


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
            