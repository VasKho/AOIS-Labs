/* #define CATCH_CONFIG_MAIN */
#include "bits.hpp"
/*#include <catch2/catch.hpp>

TEST_CASE("Addition test")
{
    Bits num_1(5);
    Bits num_2(7);
    Bits result(12);
    REQUIRE((num_1 + num_2) == result);
}*/

int main()
{
    Bits test(5);
    std::cout << test << std::endl;
    Bits test_1(10);
    std::cout << test_1 << std::endl;
    /* test.to_floating_point_format(); */
    /* std::cout << test_1.to_floating_point_format() << std::endl; */
    Bits tm(6);
    Bits tmp(-8);
    std::cout << tm + tmp << std::endl;
    std::cout << test / test_1 << std::endl;
    /* Bits result; */
    /* result = result.FP_sum(test_1, test); */
    /* std::cout << result << std::endl; */
    return 0;
}
