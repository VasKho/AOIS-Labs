#define CATCH_CONFIG_MAIN
#define CATCH_CONFIG_FAST_COMPILE
#include "bits.hpp"
#include <catch2/catch.hpp>

TEST_CASE("Simple addition test")
{
    Bits num_1(5);
    Bits num_2(7);
    Bits num_3(14);
    Bits num_4(-26);

    REQUIRE(num_1.add(num_2) == 0b1100);

    REQUIRE(num_3.add(num_4) == -0b1100);

    REQUIRE(num_4.add(num_1) == -0b10101);
}

TEST_CASE("First completion addition test")
{
    Bits num_1(5);
    Bits num_2(7);
    Bits num_3(14);
    Bits num_4(-26);

    REQUIRE(num_1.add_first_completion(num_2) == 0b1100);

    REQUIRE(num_3.add_first_completion(num_4) == -0b1100);

    REQUIRE(num_4.add_first_completion(num_1) == -0b10101);
}

TEST_CASE("Second completion addition test")
{
    Bits num_1(5);
    Bits num_2(7);
    Bits num_3(14);
    Bits num_4(-26);

    REQUIRE(num_1.add_second_completion(num_2) == 0b1100);

    REQUIRE(num_3.add_second_completion(num_4) == -0b1100);

    REQUIRE(num_4.add_second_completion(num_1) == -0b10101);
}

TEST_CASE("Simple subtraction test")
{
    Bits num_1(6);
    Bits num_2(-37);
    Bits num_3(-3);
    Bits num_4(20);

    REQUIRE(num_1.subtract(num_4) == -0b1110);

    REQUIRE(num_4.subtract(num_2) == 0b111001);

    REQUIRE(num_2.subtract(num_3) == -0b100010);

    REQUIRE(num_3.subtract(num_4) == -0b10111);
}

TEST_CASE("First completion subtraction test")
{
    Bits num_1(6);
    Bits num_2(-37);
    Bits num_3(-3);
    Bits num_4(20);

    REQUIRE(num_1.subtract_first_completion(num_4) == -0b1110);

    REQUIRE(num_4.subtract_first_completion(num_2) == 0b111001);

    REQUIRE(num_2.subtract_first_completion(num_3) == -0b100010);

    REQUIRE(num_3.subtract_first_completion(num_4) == -0b10111);
}

TEST_CASE("Second completion subtraction test")
{
    Bits num_1(6);
    Bits num_2(-37);
    Bits num_3(-3);
    Bits num_4(20);

    REQUIRE(num_1.subtract_second_completion(num_4) == -0b1110);

    REQUIRE(num_4.subtract_second_completion(num_2) == 0b111001);

    REQUIRE(num_2.subtract_second_completion(num_3) == -0b100010);

    REQUIRE(num_3.subtract_second_completion(num_4) == -0b10111);
}

TEST_CASE("Multyplication test")
{
    Bits num_1(0);
    Bits num_2(6);
    Bits num_3(-7);
    Bits num_4(10);

    REQUIRE(num_1.multiply(num_2) == 0b0);

    REQUIRE(num_3.multiply(num_2) == -0b101010);

    REQUIRE(num_2.multiply(num_4) == 0b111100);

    REQUIRE(num_4.multiply(num_3) == -0b1000110);
}

TEST_CASE("Division test with int result")
{
    Bits num_1(-27);
    Bits num_2(3);
    Bits num_3(-8);
    Bits num_4(4);

    REQUIRE(num_1.divide(num_2) == -0b1001);

    REQUIRE(num_3.divide(num_2) == -0b10);

    REQUIRE(num_1.divide(num_3) == 0b11);

    REQUIRE(num_1.divide(num_4) == -0b110);
}

TEST_CASE("Division test with float result")
{
    Bits num_1(1);
    Bits num_2(6);
    Bits num_3(-3);
    Bits num_4(-12);

    REQUIRE(num_1.divide(num_2) == 0b01010);

    REQUIRE(num_3.divide(num_2) == -0b10000);

    REQUIRE(num_3.divide(num_4) == 0b01000);

    REQUIRE(num_1.divide(num_4) == -0b00101);
}

TEST_CASE("Sum in floating point format test")
{
    Bits num_1(5);
    Bits num_2(10);
    Bits num_3(1);
    Bits num_4(0);
    num_1.to_floating_point_format();
    num_2.to_floating_point_format();
    num_3.to_floating_point_format();
    num_4.to_floating_point_format();

    REQUIRE(num_1.FP_sum(num_2) == 0b00000010011110000000000000000000);

    REQUIRE(num_3.FP_sum(num_4) == 0b00000000110000000000000000000000);

    REQUIRE(num_2.FP_sum(num_3) == 0b00000010010110000000000000000000);
}
