from typing import List


def localConsensusByN(buffer: List[str], n: int) -> List[str]:
    # returnVals
    result: List[str] = []
    ############################ \returnVals

    
    
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
            if count >= n:
                result.append(token.rstrip('\'\"'))
                break  # Only one consensus token per index

    return result