import collections

from localConsensusByN import localConsensusByN
import paho.mqtt.publish as publish
import datetime
from overlapIndex import overlapIndex

# the top level driver.  Keeps track of a minimum of state.

def driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100):
        
    # stateful vars
    
    # the number of lines we consider at a time for LocalAgreement.
    buffer = collections.deque(maxlen=BUFFER_LEN)
    for i in range(BUFFER_LEN):
        buffer.append([])
    
    # committed tokens so far.
    committed_tokens = []
    
    # for now just read from a file.  Convert this to a stream (i.e. from mqtt later)
    with open('test/data/inputs.txt', 'r') as file:
        for line in file:
            # for each loop .. we stimulate with a `line`
            
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