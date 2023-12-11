import sys
import toml
sys.path.append('./src')
from driver import driverStep

def test_driver():
    # Read the TOML file
    test_data = toml.load("./test/data/test_driver.toml")

    # Iterate over each test case
    for test_case in test_data['test']:
        lines = test_case['IN']['lines']

        # Call the driverStep function
        actual_buffer, actual_committed = driverStep(line, buffer, committed)

        # Print the results
        print("\n================================")
        print("INPUTS")
        print("------")
        print(f"line: {line}")
        print(f"buffer: {buffer}")
        print(f"committed: {committed}")
        print("OUTPUTS")
        print("-------")
        print(f"expected_buffer: {expected_buffer}")
        print(f"expected_committed: {expected_committed}")
        print("-----------------------------")
        print(f"actual_buffer: {actual_buffer}")
        print(f"actual_committed: {actual_committed}")

        # Here you can add assertions or other checks as needed

if __name__ == "__main__":
    test_driver()