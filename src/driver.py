import collections

from localConsensusByN import localConsensusByN

# the top level driver.  Keeps track of a minimum of state.

def driver(BUFFER_LEN=4, LOCAL_AGREEMENT_N=2):
        
    # stateful vars
    
    # the number of lines we consider at a time for LocalAgreement.
    buffer = collections.deque(maxlen=BUFFER_LEN)
    for i in range(BUFFER_LEN):
        buffer.append([])
    
    # for now just read from a file.  Convert this to a stream (i.e. from mqtt later)
    with open('test/data/inputs.txt', 'r') as file:
        for line in file:
            # print(line.strip())
            buffer.append(line.strip().replace('"', '').replace('\'', '').split(' '))
            
            # run overlap index
            # overlapIndex
            
            newTokens = localConsensusByN(buffer, LOCAL_AGREEMENT_N)