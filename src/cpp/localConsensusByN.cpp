#include "localConsensusByN.hpp"
#include <unordered_map>
#include <algorithm>

std::vector<std::string> localConsensusByN(const std::vector<std::vector<std::string>>& buffer, int n) {
    std::vector<std::string> result;
    if (buffer.empty()) {
        return result;
    }

    size_t max_length = 0;
    for (const auto& lst : buffer) {
        max_length = std::max(max_length, lst.size());
    }

    for (size_t i = 0; i < max_length; ++i) {
        std::unordered_map<std::string, int> token_counts;
        for (const auto& inferenceTokens : buffer) {
            if (i >= inferenceTokens.size()) {
                continue;
            }

            std::string token = inferenceTokens[i];
            std::transform(token.begin(), token.end(), token.begin(), ::tolower);
            token.erase(std::remove(token.end() - 2, token.end(), '.'), token.end());
            token.erase(std::remove(token.end() - 2, token.end(), ','), token.end());

            ++token_counts[token];
        }

        for (const auto& [token, count] : token_counts) {
            if (count >= n) {
                result.push_back(token.substr(0, token.size() - std::min(token.size(), static_cast<size_t>(2))));
                break;
            }
        }
    }

    return result;
}