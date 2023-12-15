cmake_minimum_required(VERSION 3.10)
# Set the project name and version
project(localAgreement)
# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# Add the executable for the test
add_executable(test__overlapIndex test/cpp/test_overlapIndex.cpp src/cpp/overlapIndex.cpp)
add_executable(test__localConsensusByN test/cpp/test__localConsensusByN.cpp src/cpp/localConsensusByN.cpp)
add_executable(sanity__toml test/cpp/sanity__tomlplusplus.cpp)
# Include directories where the header files are located
include_directories(src/cpp)
# If cpptoml is a header-only library and is located in the 'third_party' directory
include_directories(include)
# If cpptoml is not header-only, find and link the library
# find_package(cpptoml REQUIRED)
# target_link_libraries(overlapIndexTest cpptoml)

# include tomlplusplus
include_directories(tomlplusplus/include)