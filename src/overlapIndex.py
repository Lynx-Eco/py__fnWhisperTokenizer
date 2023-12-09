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