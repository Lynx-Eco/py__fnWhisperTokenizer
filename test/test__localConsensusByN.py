import sys
import toml
sys.path.append('./src')
from localConsensusByN import localConsensusByN

def test_localConsensusByN():
    # Read the TOML file
    test_data = toml.load("./test/data/test_localConsensusByN.toml")

    # Iterate over each test case
    for test_case in test_data['test']:
        buffer = test_case['INS']['buffer']
        n = test_case['INS']['n']
        expected_result = test_case['OUTS']['result']

        # Call the function and assert the result
        actual_result = localConsensusByN(buffer, n)

        # print expected and actual.
        print("\n================================")
        print("INPUTS")
        print("------")
        print(f"buffer: {buffer}")
        print(f"n: {n}")
        print("OUTPUTS")
        print("-------")
        print(f"expected_result: {expected_result}")
        print("-----------------------------")
        print(f"actual_result: {actual_result}")

        assert actual_result == expected_result, f"Test failed: Output {actual_result} does not match expected value {expected_result}."

if __name__ == "__main__":
    test_localConsensusByN()
    print("\nAll tests passed: Output matches expected values.")