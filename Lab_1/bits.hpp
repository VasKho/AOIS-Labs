#ifndef _BITS_H_
#define _BITS_H_
#include <iostream>
#include <bitset>
#include <math.h>

class Bits
{
    private:
        std::bitset<32> bits;
        Bits divide_int(const Bits&);
        Bits divide_float(const Bits&);
    public:
        Bits(const int& = 0);
        Bits(const Bits&);
        Bits to_floating_point_format();
        Bits to_first_completion();
        Bits to_second_completion();
        Bits add(const Bits&);
        Bits add_first_completion(const Bits&);
        Bits add_second_completion(const Bits&);
        Bits subtract(const Bits&);
        Bits subtract_first_completion(const Bits&);
        Bits subtract_second_completion(const Bits&);
        Bits multiply(const Bits&);
        Bits divide(const Bits&);
        Bits FP_sum(const Bits&);
        short compare_absolutes(const Bits&, const Bits&);
        int size() const;
        Bits operator<<(const int&);
        Bits operator>>(const int&);
        friend bool operator==(const Bits&, const Bits&);
        friend std::ostream& operator<<(std::ostream&, const Bits&);
};
#endif
