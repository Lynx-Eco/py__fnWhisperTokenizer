cmake_minimum_required(VERSION 3.10)
# Set the project name and version
project(OverlapIndexTest)
# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# Add the executable for the test
add_executable(overlapIndexTest test/test_overlapIndex.cpp src/cpp/overlapIndex.cpp)
# Include directories where the header files are located
include_directories(src/cpp)
# If cpptoml is a header-only library and is located in the 'third_party' directory
include_directories(include)
# If cpptoml is not header-only, find and link the library
# find_package(cpptoml REQUIRED)
# target_link_libraries(overlapIndexTest cpptoml)