import collections

from localConsensusByN import localConsensusByN
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
            # print(line.strip())
            buffer.append(line.strip().replace('"', '').replace('\'', '').split(' '))
            
            prompt = []
            if len(committed_tokens) > PROMPT_LEN:
                prompt = committed_tokens[-PROMPT_LEN:]
            else:
                prompt = committed_tokens
            
            candidateBuffer = [transcription[overlapIndex(prompt, transcription):] for transcription in buffer]
            
            newTokens = localConsensusByN(candidateBuffer, LOCAL_AGREEMENT_N)
            
            committed_tokens.extend(newTokens)