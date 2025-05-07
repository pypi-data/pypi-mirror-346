add_executable(
        unit_test
        test_double.cpp
        test_decimal.cpp)

target_link_libraries(unit_test PUBLIC gtest_main gmock_main FastLanes)
gtest_discover_tests(unit_test)

target_compile_options(unit_test
        PRIVATE
        "-fsanitize=address"
        "-fsanitize=undefined")

target_link_options(unit_test
        PRIVATE
        "-fsanitize=address"
        "-fsanitize=undefined")


