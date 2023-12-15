#include <iostream>
#include <vector>
#include <cassert>
#include <string>
#include "localConsensusByN.hpp" // Assuming the function is declared in this header

// #include "../../tomlplusplus/examples/examples.hpp"
#include <toml++/toml.hpp>

#include <string_view>

using namespace std::string_view_literals;

void test_localConsensusByN() {
    try {
        auto config = toml::parse_file("../test/data/test_localConsensusByN.toml");
        auto tests = config["test"].as_array();

        for (auto& test_table : *tests) {
            toml::table ins = *test_table["INS"sv].as_table();
            toml::table outs = *test_table["OUTS"sv].as_table();

            std::vector<std::vector<std::string>> buffer;
            for (const auto& line : *ins["buffer"sv].as_array()) {
                std::vector<std::string> line_data;
                for (const auto& value : line.as_array()) {
                    line_data.push_back(value.value_or(""sv));
                }
                buffer.push_back(line_data);
            }
            int n = ins["n"sv].value_or(0);
            std::vector<std::string> expected_result;
            for (const auto& value : outs["result"sv].as_array()) {
                expected_result.push_back(value.value_or(""sv));
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
    } catch (const toml::parse_error& err) {
        std::cerr << "TOML parse error: " << err << std::endl;
        exit(1);
    }
}

int main() {
    test_localConsensusByN();
    std::cout << "\nAll tests passed: Output matches expected values." << std::endl;
    return 0;
}