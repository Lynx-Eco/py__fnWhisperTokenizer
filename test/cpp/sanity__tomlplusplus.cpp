#include <iostream>
#include <toml.hpp>

int main() {
    try {
        auto data = toml::parse("./include/toml.hpp");

        // Assuming toml.hpp contains a table we can iterate over
        // This is just an example and may need to be adapted to the actual TOML structure
        for (const auto& [key, value] : *data.as_table()) {
            std::cout << "Key: " << key << ", Value: " << value << std::endl;
        }
    } catch (const toml::parse_error& err) {
        std::cerr << "Parsing failed: " << err << std::endl;
        return 1;
    }

    return 0;
}