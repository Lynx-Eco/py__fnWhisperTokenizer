#include "driver.hpp"
#include "localConsensusByN.hpp"
#include "overlapIndex.hpp"
#include <algorithm>
#include <iostream>
#include <sstream>

driver::driver(int BUFFER_LEN, int LOCAL_AGREEMENT_N, int PROMPT_LEN)
    : LOCAL_AGREEMENT_N(LOCAL_AGREEMENT_N), PROMPT_LEN(PROMPT_LEN), DEBUG(false), lines_read(0) {
    for (int i = 0; i < BUFFER_LEN; ++i) {
        ctxBuffer.emplace_back();
    }
}

std::tuple<std::vector<std::string>, std::deque<std::vector<std::string>>, std::vector<std::string>> driver::drive(const std::string& line) {
    // Tokenize and insert the line into the buffer
    std::vector<std::string> lineSanitizedTokens;
    std::istringstream iss(line);
    for (std::string token; iss >> token;) {
        lineSanitizedTokens.push_back(token);
    }
    ctxBuffer.push_back(lineSanitizedTokens);

    // Prepare prompt
    std::vector<std::string> prompt;
    if (committed_tokens.size() > PROMPT_LEN) {
        prompt.assign(committed_tokens.end() - PROMPT_LEN, committed_tokens.end());
    } else {
        prompt = committed_tokens;
    }

    // Get new tokens using the driver step function
    std::vector<std::string> newTokens = fnDriverStep(prompt, ctxBuffer, LOCAL_AGREEMENT_N);
    committed_tokens.insert(committed_tokens.end(), newTokens.begin(), newTokens.end());

    if (DEBUG) {
        std::cout << "drive with line: " << line << std::endl;
        std::cout << "prompt: ";
        for (const auto& token : prompt) std::cout << token << ' ';
        std::cout << "\nctxBuffer size: " << ctxBuffer.size() << std::endl;
        std::cout << "newTokens: ";
        for (const auto& token : newTokens) std::cout << token << ' ';
        std::cout << std::endl;
    }

    return {newTokens, ctxBuffer, committed_tokens};
}

std::vector<std::string> driver::fnDriverStep(const std::vector<std::string>& prompt, const std::deque<std::vector<std::string>>& buffer, int LOCAL_AGREEMENT_N) {
    std::vector<std::vector<std::string>> candidateBuffer;
    for (const auto& transcription : buffer) {
        candidateBuffer.push_back(std::vector<std::string>(transcription.begin() + overlapIndex(prompt, transcription), transcription.end()));
    }

    return localConsensusByN(candidateBuffer, LOCAL_AGREEMENT_N);
}