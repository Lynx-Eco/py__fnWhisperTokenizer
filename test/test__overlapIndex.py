import sys
import toml
sys.path.append('./src')
from overlapIndex import overlapIndex

def test_overlapIndex():
    # Read the TOML file
    test_data = toml.load("./test/data/test_0.toml")

    # Extract inputs and expected output
    prompt = test_data['INPUTS']['prompt']
    transcription = test_data['INPUTS']['transcription']
    expected_idx = test_data['OUTPUTS']['idx']

    # Call the function and assert the result
    assert overlapIndex(prompt, transcription) == expected_idx, "Test failed: Output index does not match expected value."

if __name__ == "__main__":
    test_overlapIndex()
    print("Test passed: Output index matches expected value.")
