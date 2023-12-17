#ifndef DRIVER_HPP
#define DRIVER_HPP

#include <string>
#include <vector>
#include <deque>

class driver {
public:
    driver(int BUFFER_LEN = 4, int LOCAL_AGREEMENT_N = 2, int PROMPT_LEN = 100);
    std::tuple<std::vector<std::string>, std::deque<std::vector<std::string>>, std::vector<std::string>> drive(const std::string& line);

private:
    std::deque<std::vector<std::string>> ctxBuffer;
    int LOCAL_AGREEMENT_N;
    int PROMPT_LEN;
    std::vector<std::string> committed_tokens;
    bool DEBUG;
    int lines_read;

    static std::vector<std::string> fnDriverStep(const std::vector<std::string>& prompt, const std::deque<std::vector<std::string>>& buffer, int LOCAL_AGREEMENT_N);
};

#endif // DRIVER_HPP