import collections
from typing import List

from localConsensusByN import localConsensusByN
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime
from overlapIndex import overlapIndex


# entry point to the driver.  Settings for meta params.
class driver:
    def __init__(self, BUFFER_LEN=4, LOCAL_AGREEMENT_N=2, PROMPT_LEN=100):
        # the number of lines we consider at a time for LocalAgreement.
        self.ctxBuffer: List[List[str]] = collections.deque(maxlen=BUFFER_LEN)
        for i in range(BUFFER_LEN):
            self.ctxBuffer.append([])
        self.LOCAL_AGREEMENT_N = LOCAL_AGREEMENT_N
        self.PROMPT_LEN = PROMPT_LEN
        
        # committed tokens so far.
        self.committed_tokens: List[str] = []
        
        self.DEBUG = False
        self.lines_read = 0
        
    # primary entry point for driver. stimulate with a transcription line
    def drive(self, line: str) -> (List[str], List[List[str]], List[str]):
        def insertLineIntoCircularBufferOfToken(line: str, buffer: List[str]):
            lineSanitizedTokens = line.strip().replace('"', '').replace('\'', '').split(' ')
            buffer.append(lineSanitizedTokens)
            return buffer
        
        # prepare inputs
        
        # tokenize and write the line into the buffer.
        self.ctxBuffer = insertLineIntoCircularBufferOfToken(line, self.ctxBuffer)
        
        # prepare prompt.
        prompt = []
        if len(self.committed_tokens) > self.PROMPT_LEN:
            prompt = self.committed_tokens[-self.PROMPT_LEN:].copy()
        else:
            prompt = self.committed_tokens.copy()
            
        newTokens: List[str] = self.fnDriverStep(prompt, self.ctxBuffer, self.LOCAL_AGREEMENT_N)
        self.committed_tokens.extend(newTokens)
        
        if self.DEBUG:
            print("======================")
            print("drive with line:")
            print(line)
            print("prompt:")
            print(prompt)
            print()
            print("ctxBuffer:")
            print(self.ctxBuffer)
            print()
            print("result - newTokens:")
            print(newTokens)
            
            print()
            print()
        
        return (newTokens, self.ctxBuffer, self.committed_tokens)
        

    # pure functions below this point.  They take inputs and outputs.
    @staticmethod
    def fnDriverStep(prompt: List[str], buffer: List[str], LOCAL_AGREEMENT_N: int) -> (List[str]):
        # this one liner filters buffer down to candidateBuffer
        candidateBuffer = [transcription[overlapIndex(prompt, transcription):] for transcription in buffer]
        
        newTokens = localConsensusByN(prompt, candidateBuffer, LOCAL_AGREEMENT_N)
        
        # a side effect! perhaps we should move it?
        if len(newTokens):
            # emit `newTokens` to `whisper/confirmedTokens` here.
            # Format the current datetime as ISO 8601
            now_iso = datetime.datetime.now().isoformat()
            # Convert `newTokens` to a string and publish the message
            message = f"{now_iso} {newTokens}"
            publish.single("whisper/confirmedTokens", message, hostname="localhost")
        
        return newTokens
        # at the end of each loop .. we have a new committed string..