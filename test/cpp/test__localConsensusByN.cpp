#include <iostream>
#include <vector>
#include <cassert>
#include <string>
#include "localConsensusByN.hpp" // Assuming the function is declared in this header
#include <cpptoml.h>


void test_localConsensusByN() {
    // auto config = cpptoml::parse_file("./test/data/test_localConsensusByN.toml");
    auto config = cpptoml::parse_file("../test/data/test_localConsensusByN.toml");
    auto tests = config->get_table_array("test");

    for (const auto& test_table : *tests) {
        auto ins = test_table->get_table("INS");
        auto outs = test_table->get_table("OUTS");

        std::vector<std::vector<std::string>> buffer;
        auto buffer_array = ins->get_array_of<cpptoml::array>("buffer");
        if (buffer_array) {
            for (const auto& line : *buffer_array) {
                std::vector<std::string> line_data;
                for (const auto& value : *line) {
                    line_data.push_back(value->as<std::string>()->get());
                }
                buffer.push_back(line_data);
            }
        } else {
            std::cerr << "Error reading buffer from TOML file." << std::endl;
        }
        int n = *ins->get_as<int>("n");
        std::vector<std::string> expected_result;
        for (const auto& value : *outs->get_array_of<std::string>("result")) {
            expected_result.push_back(value);
        }

        std::vector<std::string> actual_result = localConsensusByN(buffer, n);

        std::cout << "\n================================" << std::endl;
        std::cout << "INPUTS" << std::endl;
        std::cout << "------" << std::endl;
        std::cout << "buffer: ";
        for (const auto& line : buffer) {
            for (const auto& val : line) {
                std::cout << val << " ";
            }
            std::cout << std::endl;
        }
        std::cout << "n: " << n << std::endl;
        std::cout << "OUTPUTS" << std::endl;
        std::cout << "-------" << std::endl;
        std::cout << "expected_result: ";
        for (const auto& val : expected_result) {
            std::cout << val << " ";
        }
        std::cout << "\n-----------------------------" << std::endl;
        std::cout << "actual_result: ";
        for (const auto& val : actual_result) {
            std::cout << val << " ";
        }
        std::cout << std::endl;

        assert(actual_result == expected_result && "Test failed: Output does not match expected value.");
    }
}

int main() {
    test_localConsensusByN();
    std::cout << "\nAll tests passed: Output matches expected values." << std::endl;
    return 0;
}