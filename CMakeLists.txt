cmake_minimum_required(VERSION 3.14)
project(Stack_AutoTest)

# GoogleTest requires at least C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#link_directories("/usr/local/lib")

# Set CMP0135 policy to NEW
cmake_policy(SET CMP0135 NEW)

# find_package(GTest REQUIRED)
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
#set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
enable_testing()

# message("GTest_INCLUDE_DIRS = ${GTest_INCLUDE_DIRS}")
# message("GTest_LIBRARIES = ${GTest_LIBRARIES}")

add_executable(
  main
  main.cpp 
)

add_executable(
  AutoTest_gtests
  AutoTest_gtests.cpp 
)

target_link_libraries(
  AutoTest_gtests
  GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(AutoTest_gtests)
