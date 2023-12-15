#include "../src/cpp/overlapIndex.hpp"
#include <iostream>
#include <vector>
#include <string>
#include <cassert>
#include <cpptoml.h>

void test_overlapIndex() {
    auto config = cpptoml::parse_file("./test/data/test_overlapIndex.toml");
    // auto config = cpptoml::parse_file("../test/data/test_overlapIndex.toml");
    auto tests = config->get_table_array("tests");

    for (const auto& test : *tests) {
        auto inputs = test->get_table("INPUTS");
        auto outputs = test->get_table("OUTPUTS");

        std::vector<std::string> prompt = *inputs->get_array_of<std::string>("prompt");
        std::vector<std::string> transcription = *inputs->get_array_of<std::string>("transcription");
        int expected_idx = *outputs->get_as<int>("idx");

        int result_idx = overlapIndex(prompt, transcription);

        std::cout << "\n================================" << std::endl;
        std::cout << "INPUTS" << std::endl;
        std::cout << "------" << std::endl;
        std::cout << "prompt: ";
        for (const auto& word : prompt) std::cout << word << " ";
        std::cout << std::endl;
        std::cout << "transcription: ";
        for (const auto& word : transcription) std::cout << word << " ";
        std::cout << std::endl;
        std::cout << "OUTPUTS" << std::endl;
        std::cout << "-------" << std::endl;
        std::cout << "expected_idx: " << expected_idx << std::endl;
        std::cout << "result_idx: " << result_idx << std::endl;
        std::cout << "=============================" << std::endl;

        assert(result_idx == expected_idx && "Test failed: Output index does not match expected value.");
    }
}

int main() {
    test_overlapIndex();
    std::cout << "\nAll tests passed: Output indexes match expected values." << std::endl;
    return 0;
}