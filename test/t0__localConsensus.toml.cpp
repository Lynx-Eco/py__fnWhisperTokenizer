#include "../src/cpp/localConsensusByN.hpp"
#include "../tomlplusplus/include/toml++/toml.hpp"
#include <iostream>
#include <vector>
#include <string>

int main() {
    try {
#include "../src/cpp/localConsensusByN.hpp"
#include "../tomlplusplus/include/toml++/toml.hpp"
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    try {
        auto data = toml::parse_file("test/data/localConsensusByN/t0__localConsensus.toml");
        auto buffer = data["buffer"].as_array();
        int64_t n = data["n"].value_or(-777);

        vector<vector<string>> bufferVec;
        for (const auto& line : *buffer) {
            vector<string> lineVec;
            for (const auto& word : *line.as_array()) {
                lineVec.push_back(word.as_string().str);
            }
            bufferVec.push_back(lineVec);
        }

        vector<string> result = localConsensusByN(bufferVec, n);
        vector<string> expected = data["return"].as_array()->as_vector<string>();

        bool success = result == expected;
        cout << "Test " << (success ? "PASSED" : "FAILED") << ": ";
        for (const auto& word : result) {
            cout << word << ' ';
        }
        cout << endl;
    } catch (const toml::parse_error& err) {
        cerr << "Parsing failed: " << err << endl;
        return 1;
    } catch (const exception& err) {
        cerr << "Unhandled exception: " << err.what() << endl;
        return 1;
    }

    return 0;
}
    }

    return 0;
}