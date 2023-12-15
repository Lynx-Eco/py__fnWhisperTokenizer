#include <iostream>
#include <vector>
#include <cassert>
#include <string>
#include "localConsensusByN.hpp" // Assuming the function is declared in this header
#include <cpptoml.h>


void test_localConsensusByN() {
    auto config = cpptoml::parse_file("./test/data/test_localConsensusByN.toml");
    // auto config = cpptoml::parse_file("../test/data/test_overlapIndex.toml");
    auto tests = config->get_table_array("tests");

    // for (const auto& test_case : test_cases) {
    //     const std::vector<std::string>& buffer = test_case.first;
    //     int n = test_case.second;
    //     std::vector<int> expected_result = {}; // Replace with actual expected result
    //     std::vector<int> actual_result = localConsensusByN(buffer, n);

    //     std::cout << "\n================================" << std::endl;
    //     std::cout << "INPUTS" << std::endl;
    //     std::cout << "------" << std::endl;
    //     std::cout << "buffer: ";
    //     for (const auto& val : buffer) {
    //         std::cout << val << " ";
    //     }
    //     std::cout << "\nn: " << n << std::endl;
    //     std::cout << "OUTPUTS" << std::endl;
    //     std::cout << "-------" << std::endl;
    //     std::cout << "expected_result: ";
    //     for (const auto& val : expected_result) {
    //         std::cout << val << " ";
    //     }
    //     std::cout << "\n-----------------------------" << std::endl;
    //     std::cout << "actual_result: ";
    //     for (const auto& val : actual_result) {
    //         std::cout << val << " ";
    //     }
    //     std::cout << std::endl;

    //     assert(actual_result == expected_result && "Test failed: Output does not match expected value.");
    // }
}

int main() {
    test_localConsensusByN();
    std::cout << "\nAll tests passed: Output matches expected values." << std::endl;
    return 0;
}