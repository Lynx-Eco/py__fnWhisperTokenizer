import sys
import toml
sys.path.append('./src')
from overlapIndex import overlapIndex

def test_overlapIndex():
    # Read the TOML file
    test_data = toml.load("./test/data/test_overlapIndex.toml")

    # Iterate over each test case
    for test_case in test_data['tests']:
        prompt = test_case['INPUTS']['prompt']
        transcription = test_case['INPUTS']['transcription']
        expected_idx = test_case['OUTPUTS']['idx']

        result_idx = overlapIndex(prompt, transcription)
        
        # print expected and actual.
        print("\n================================")
        print("INPUTS")
        print("------")
        print(f"prompt: {prompt}")
        print(f"transcription: {transcription}")
        print("OUTPUTS")
        print("-------")
        print(f"expected_idx: {expected_idx}")
        print("-----------------------------")
        print(f"result_idx: {result_idx}")
        
        # the operative useful tokens out are as follows:
        new_candidate_tokens = transcription[result_idx:]
        print(f"{new_candidate_tokens}")
        
        
        # Call the function and assert the result
        assert result_idx == expected_idx, f"Test failed: Output index {overlapIndex(prompt, transcription)} does not match expected value {expected_idx}."

if __name__ == "__main__":
    test_overlapIndex()
    print("\nAll tests passed: Output indexes match expected values.")
