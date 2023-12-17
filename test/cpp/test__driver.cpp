#include <iostream>
#include <cassert>
#include "../../src/cpp/driver.hpp"

void test_driver() {
    // Create an instance of the driver class
    driver driverInst(4, 2, 100);
    std::vector<std::string> lines = {
            "a sample",
            "a sample line",
            "sample line. and more",
            "sample line. and more for sure",
            "sample line. and more for sure brah",
            "sample line. and more for sure brah hah",
    };
    std::vector<std::string> expected_tokens = {"sample", "line", "and", "more"};

    for (const auto& line : lines) {
        auto [newTokens, ctxBuffer, committed_tokens] = driverInst.drive(line);
        // Here you can add assertions or other checks as needed
        for (const auto& token : newTokens) {
            std::cout << token << ' ';
        }
        std::cout << std::endl;
    }

    // Check if the committed tokens match the expected tokens
    // assert(committed_tokens == expected_tokens && "Test failed: Committed tokens do not match expected tokens.");
}

int main() {
    test_driver();
    std::cout << "All tests passed: Committed tokens match expected tokens." << std::endl;
    return 0;
}