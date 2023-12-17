#include "../src/cpp/localConsensusByN.hpp"
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    // Statically coded input based on t0__localConsensus.toml
    const vector<vector<string>> buffer = {
        {"frog", "walk", "into", "a", "cafe."},
        {},
        {"robber", "sitting", "alone", "in", "the", "corner."},
        {"robber", "sitting", "alone", "at", "a", "table."}
    };
    const int n = 2;

    // Expected output
    const vector<string> expected = {"robber", "sitting", "alone"};

    // Test execution
    vector<string> result = localConsensusByN(buffer, n);

    // Test comparison
    bool success = result == expected;
    cout << "Test " << (success ? "PASSED" : "FAILED") << ": ";
    for (const auto& word : result) {
        cout << word << ' ';
    }
    cout << endl;

    return success ? 0 : 1;
}