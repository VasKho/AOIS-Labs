#ifndef _BITS_H_
#define _BITS_H_
#include <iostream>
#include <bitset>
#include <math.h>

class Bits
{
    private:
        std::bitset<32> bits;
        Bits add(const Bits&, const Bits&);
        Bits add_first_completion(Bits, Bits);
        Bits add_second_completion(Bits, Bits);
        Bits subtract(const Bits&, const Bits&);
        Bits subtract_first_completion(Bits, Bits);
        Bits subtract_second_completion(Bits, Bits);
        short compare_absolutes(const Bits&, const Bits&);
        Bits multiply(const Bits&, const Bits&);
        Bits divide(const Bits&, const Bits&);
        int size() const;
    public:
        Bits(const int& = 0);
        Bits(const Bits&);
        Bits FP_sum(const Bits&, const Bits&);
        Bits to_floating_point_format();
        Bits to_first_completion();
        Bits to_second_completion();
        friend std::ostream& operator<<(std::ostream&, const Bits&);
        friend Bits operator+(const Bits&, const Bits&);
        friend Bits operator-(const Bits&, const Bits&);
        friend Bits operator*(const Bits&, const Bits&);
        friend Bits operator/(const Bits&, const Bits&);
        friend bool operator==(const Bits&, const Bits&);
        Bits operator<<(const int&);
        Bits operator>>(const int&);
};
#endif
