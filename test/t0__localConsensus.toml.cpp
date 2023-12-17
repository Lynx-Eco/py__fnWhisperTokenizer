#include "../src/cpp/localConsensusByN.hpp"
#include "../tomlplusplus/include/toml++/toml.hpp"
#include <iostream>
#include <vector>
#include <string>

int main() {
    try {
        auto data = toml::parse_file("test/data/localConsensusByN/t0__localConsensus.toml");
        auto buffer = data["buffer"].as_array();
        int64_t n = data["n"].value_or(-777);

        std::vector<std::vector<std::string>> bufferVec;
        for (const auto& line : *buffer) {
            std::vector<std::string> lineVec;
            for (const auto& word : *line.as_array()) {
                lineVec.push_back(word.as_string().str);
            }
            bufferVec.push_back(lineVec);
        }

        std::vector<std::string> result = localConsensusByN(bufferVec, n);
        std::vector<std::string> expected = data["return"].as_array()->as_vector<std::string>();

        bool success = result == expected;
        std::cout << "Test " << (success ? "PASSED" : "FAILED") << ": ";
        for (const auto& word : result) {
            std::cout << word << ' ';
        }
        std::cout << std::endl;
    } catch (const toml::parse_error& err) {
        std::cerr << "Parsing failed: " << err << std::endl;
        return 1;
    } catch (const std::exception& err) {
        std::cerr << "Unhandled exception: " << err.what() << std::endl;
        return 1;
    }

    return 0;
}