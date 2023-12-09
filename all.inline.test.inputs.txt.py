import collections

def printdeq(deq):
    print('[')
    for elt in deq:
        print(elt)
    print(']')

def zip_last_first(prompt, transcription, n):
    # Zip the last n elements of `prompt` with the first n elements of `transcription`
    return list(zip(prompt[-n:], transcription[:n]))

def count_matching_tuples(tuples_list):
    # Function to remove periods and commas, and to make the string lowercase
    def clean_string(s):
        return s.replace('.', '').replace(',', '').lower()

    # Count the number of tuples where the cleaned strings match
    return sum([clean_string(left) == clean_string(right) for left, right in tuples_list])


bestMatch = 0
bestMatchIndex = 0
def overlapIndex(prompt, transcription):
    maxOverlap = min(len(prompt), len(transcription))
    bestMatch = 0
    bestMatchIndex = 0
    for i in range(1, maxOverlap + 1):
        thisZip = zip_last_first(prompt, transcription, i)
        # thisMatches = count_matching_tuples(thisZip)
        thisMatches = count_matching_tuples(thisZip)
        if thisMatches > bestMatch:
            bestMatch = thisMatches
            bestMatchIndex = i
    return bestMatchIndex

    

# def findConsensusTokens(buffer):
#     # Initialize the result list
#     result = []
#     # Check if buffer is not empty and contains lists
#     if not buffer or not all(isinstance(lst, list) for lst in buffer):
#         return result
#     # Find the minimum length of the lists in buffer to avoid index errors
#     min_length = min(len(lst) for lst in buffer)
#     # Iterate over the range of the shortest list
#     for i in range(min_length):
#         # Create a dictionary to count occurrences of each standardized token
#         token_counts = {}
#         original_tokens = {}
#         # Iterate over each list in the buffer
#         for inferenceTokens in buffer:
#             # Standardize the token by lowercasing and stripping punctuation
#             standardized_token = inferenceTokens[i].lower().rstrip('.,')
#             # Store the original token
#             original_tokens[standardized_token] = inferenceTokens[i]
#             # Increment the token count
#             token_counts[standardized_token] = token_counts.get(standardized_token, 0) + 1
#         # Find tokens with a count of at least two and append the original token to result
#         for standardized_token, count in token_counts.items():
#             if count >= 2:
#                 result.append(original_tokens[standardized_token])
#                 break  # Only one consensus token per index
#     return result

# case insensitive
def findConsensusTokens(buffer):
    # Initialize the result list
    result = []
    # Check if buffer is not empty and contains lists
    if not buffer or not all(isinstance(lst, list) for lst in buffer):
        return result
    # Find the minimum length of the lists in buffer to avoid index errors
    # min_length = min(len(lst) for lst in buffer)
    
    max_length = max(len(lst) for lst in buffer)
    # Iterate over the range of the shortest list
    # for i in range(min_length):
    for i in range(max_length):
        # Create a dictionary to count occurrences of each token
        token_counts = {}
        # Iterate over each list in the buffer
        for inferenceTokens in buffer:
            # Standardize the token by lowercasing and stripping punctuation
            
            # if were off the end of this token buffer move on..
            if i >= len(inferenceTokens):
                continue
            
            token = inferenceTokens[i].lower().rstrip('.,')
            # Increment the token count
            token_counts[token] = token_counts.get(token, 0) + 1
        # Find tokens with a count of at least two and append to result
        for token, count in token_counts.items():
            if count >= 2:
                result.append(token)
                break  # Only one consensus token per index
    return result


confirmedStr = ""
confirmedTokens = []
def processBuffer(buf):
    global confirmedTokens

    # prompt = confirmedStr.strip().split(' ')
    prompt = confirmedTokens
    
    newTokens = []
    for elt in buf:
        idx = overlapIndex(prompt, elt)
        newTokens.append(elt[idx:])
        print(f"overlap: {idx}")
    
    printdeq(newTokens)
    
    consensusTokens = findConsensusTokens(newTokens)
    print(f"\nCONSENSUS THIS ROUND: {consensusTokens}")
    
    confirmedTokens += consensusTokens
    print(f"CONFIRMED ALL TIME: {confirmedTokens}")
    

def build_context_buffer(filename):
    buffer = collections.deque(maxlen=4)
    with open(filename, 'r') as file:
        for line in file:
            print("\n\n================================================")
            print("reading line " + str(line))
            print()
            buffer.append(line.strip().split(' '))
            # process the current buffer
            processBuffer(buffer)
            printdeq(buffer)
    return list(buffer)

if __name__ == '__main__':
    context = build_context_buffer('test/data/inputs.txt')
    # print(context)
