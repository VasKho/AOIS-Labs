#include "bits.hpp"


Bits Bits::add(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    if(num_1.bits[31] == num_2.bits[31])
    {
        result.bits[31] = num_1.bits[31];
        bool carry = 0;
        for(int i = 0; i < 31; ++i)
        {
            result.bits[i] = (num_1.bits[i] ^ num_2.bits[i]) ^ carry;
            carry = (num_1.bits[i] & num_2.bits[i]) | (num_1.bits[i] & carry) | (num_2.bits[i] & carry);
        }
    }
    else
    {
        Bits max, min;
        if(compare_absolutes(num_1, num_2) == 1)
        {
            max = num_1;
            min = num_2;
        }
        else
        {
            max = num_2;
            min = num_1;
        }
        Bits max_abs, min_abs;
        max_abs = max;
        max_abs.bits[31] = 0;
        min_abs = min;
        min_abs.bits[31] = 0;
        result = subtract(max_abs, min_abs);
        if(num_1.bits[31] == 0)
        {
            if(num_1 == max) result.bits[31] = 0;
            else result.bits[31] = 1;
        }
        else
        {
            if(num_1 == max) result.bits[31] = 1;
            else result.bits[31] = 0;
        }
    }
    return result;
}

Bits Bits::add_first_completion(Bits num_1, Bits num_2)
{
    if(num_1.bits[31] == 1) num_1.to_first_completion();
    if(num_2.bits[31] == 1) num_2.to_first_completion();
    Bits result;
    bool carry = 0;
    for(int i = 0; i < 32; ++i)
    {
        result.bits[i] = (num_1.bits[i] ^ num_2.bits[i]) ^ carry;
        carry = (num_1.bits[i] & num_2.bits[i]) | (num_1.bits[i] & carry) | (num_2.bits[i] & carry);
    }
    if(carry)
    {
        for(int i = 0; i < 32; ++i)
        {
            result.bits[i] = (num_1.bits[i] ^ num_2.bits[i]) ^ carry;
            carry = (num_1.bits[i] & num_2.bits[i]) | (num_1.bits[i] & carry) | (num_2.bits[i] & carry);
        }
    }
    if(result.bits[31] == 1)
        for(int i = 0; i < 31; ++i) result.bits[i] = ~result.bits[i];
    return result;
}

Bits Bits::add_second_completion(Bits num_1, Bits num_2)
{
    if(num_1.bits[31] == 1) num_1.to_second_completion();
    if(num_2.bits[31] == 1) num_2.to_second_completion();
    Bits result;
    bool carry = 0;
    for(int i = 0; i < 32; ++i)
    {
        result.bits[i] = (num_1.bits[i] ^ num_2.bits[i]) ^ carry;
        carry = (num_1.bits[i] & num_2.bits[i]) || (num_1.bits[i] & carry) || (num_2.bits[i] & carry);
    }
    if(result.bits[31] == 1)
    {
        Bits n_one(1);
        result = add(result, n_one);
        for(int i = 0; i < 31; ++i) result.bits[i] = ~result.bits[i];
    }
    return result;
}

Bits Bits::subtract(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    if(num_1.bits[31] == num_2.bits[31])
    {
        result.bits[31] = num_1.bits[31];
        bool carry = 0;
        for(int i = 0; i < 31; ++i)
        {
            if(carry)
            {
                result.bits[i] = !(num_1.bits[i] ^ num_2.bits[i]);
                carry = !num_1.bits[i] | (num_1.bits[i] & num_2.bits[i]);
            }
            else
            {
                result.bits[i] = num_1.bits[i] ^ num_2.bits[i];
                carry = !num_1.bits[i] & num_2.bits[i];
            }
        }
    }
    else
    {
        Bits max, min;
        if(compare_absolutes(num_1, num_2) == 1)
        {
            max = num_1;
            min = num_2;
        }
        else
        {
            max = num_2;
            min = num_1;
        }
        Bits max_abs, min_abs;
        max_abs = max;
        max_abs.bits[31] = 0;
        min_abs = min;
        min_abs.bits[31] = 0;
        result = add(max_abs, min_abs);
        if(num_1 == max)
        {
            if(max.bits[31] == 0) result.bits[31] = 0;
            else result.bits[31] = 1;
        }
        else
        {
            if(min.bits[31] == 0) result.bits[31] = 0;
            else result.bits[31] = 1;
        }
    }
    return result;
}

Bits Bits::subtract_first_completion(Bits num_1, Bits num_2)
{
    Bits result;
    if(num_1.bits[31] == 0 && num_2.bits[31] == 1)
    {
        num_2.bits[31] = 0;
        result = add_first_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 1 && num_2.bits[31] == 0)
    {
        num_2.bits[31] = 1;
        result = add_first_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 0 && num_2.bits[31] == 0)
    {
        num_2.bits[31] = 1;
        result = add_first_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 1 && num_2.bits[31] == 1)
    {
        num_2.bits[31] = 0;
        result = add_first_completion(num_1, num_2);
    }
    return result;
}

Bits Bits::subtract_second_completion(Bits num_1, Bits num_2)
{
    Bits result;
    if(num_1.bits[31] == 0 && num_2.bits[31] == 1)
    {
        num_2.bits[31] = 0;
        result = add_second_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 1 && num_2.bits[31] == 0)
    {
        num_2.bits[31] = 1;
        result = add_second_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 0 && num_2.bits[31] == 0)
    {
        num_2.bits[31] = 1;
        result = add_second_completion(num_1, num_2);
    }
    else if(num_1.bits[31] == 1 && num_2.bits[31] == 1)
    {
        num_2.bits[31] = 0;
        result = add_second_completion(num_1, num_2);
    }
    return result;
}

Bits Bits::multiply(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    for(int num_2_iter = 0; num_2_iter < 31; ++num_2_iter)
    {
        Bits temp;
        for(int num_1_iter = 0; num_1_iter < 31; ++num_1_iter)
        {
            temp.bits[num_1_iter] = num_1.bits[num_1_iter] & num_2.bits[num_2_iter];
        }
        result = add(result, temp << num_2_iter);
    }
    result.bits[31] = num_1.bits[31] ^ num_2.bits[31];
    return result;
}

Bits Bits::divide(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    Bits divident(num_1);
    divident.bits[31] = 0;
    Bits divisor(num_2);
    divisor.bits[31] = 0;
    int divident_size = divident.size();
    int divisor_size = num_2.size();
    if(divisor_size < 0)
    {
        std::cout << "DivisionByZero" << std::endl;
        exit(1);
    }
    int divisor_shift = divident_size - divisor_size;
    divisor << divisor_shift;
    Bits neg_divisor = divisor;
    neg_divisor.bits[31] = 1;
    divisor.bits[31] = 1;
    Bits remaining = divident;
    Bits zero(0);
    for(int res_bit = divisor_shift; res_bit >= 0; --res_bit)
    {
        if(remaining.bits[31] == 1) remaining = add(remaining, divisor);
        else 
        {
            remaining = add_second_completion(remaining, neg_divisor);
            remaining.to_second_completion();
        }
        if(remaining.bits[31] == 1 && compare_absolutes(remaining, zero) != 0) result.bits[res_bit] = 0;
        else result.bits[res_bit] = 1;
        remaining << 1;
    }
    if((num_1.bits[31] ^ num_2.bits[31]) == 1) result.bits[31] = 1;
    return result;
}

Bits Bits::FP_sum(const Bits& num_1, const Bits& num_2)
{
    Bits min = num_2, max = num_1;
    Bits result;
    for(int exp_iter = 30; exp_iter >= 23; --exp_iter)
    {
        if(num_1.bits[exp_iter] != num_2.bits[exp_iter])
        {
            if(num_1.bits[exp_iter] == 1)
            {
                max = num_1;
                min = num_2;
            }
            else
            {
                max = num_2;
                min = num_1;
            }
            break;
        }
    }
    bool borrow = 0;
    std::bitset<32> exponent;
    for(int i = 23; i < 31; ++i)
    {
        if(borrow)
        {
            exponent[i] = !(max.bits[i] ^ min.bits[i]);
            borrow = !max.bits[i] | (max.bits[i] & min.bits[i]);
        }
        else
        {
            exponent[i] = max.bits[i] ^ min.bits[i];
            borrow = !max.bits[i] & min.bits[i];
        }
    }
    bool carry = 0;
    std::cout << min << std::endl;
    for(int i = 23; i < 31; ++i)
    {
        result.bits[i] = (min.bits[i] ^ exponent[i]) ^ carry;
        carry = (min.bits[i] & exponent[i]) | (min.bits[i] & carry) | (exponent[i] & carry);
    }
    int decimal_shift = 0;
    for(int i = 23; i < 31; ++i) decimal_shift += exponent[i] * pow(2, i - 23);
    for(int i = 0; i <= 22; ++i) 
    {
        if((i + decimal_shift) > 22) min.bits[i] = 0;
        else min.bits[i] = min.bits[i + decimal_shift];
    }
    for(int i = 0; i < 23; ++i)
    {
        result.bits[i] = (min.bits[i] ^ max.bits[i]) ^ carry;
        carry = (min.bits[i] & max.bits[i]) | (min.bits[i] & carry) | (max.bits[i] & carry);
    }
    if(carry)
    {
        for(int i = 0; i < 23; ++i) result.bits[i] = result.bits[i + 1];
        result.bits[22] = 1;
        std::bitset<32> one{0b00000000100000000000000000000000};
        carry = 0;
        for(int i = 23; i < 31; ++i)
        {
            result.bits[i] = (max.bits[i] ^ one[i]) ^ carry;
            carry = (max.bits[i] & one[i]) | (max.bits[i] & carry) | (one[i] & carry);
        }
    }
    std::cout << min << std::endl;
    std::cout << max << std::endl;
    return result;
}

int Bits::size() const
{
    int size = 30;
    for(; size >= 0; --size) if(this->bits[size]) break;
    return size;
}

short Bits::compare_absolutes(const Bits& num_1, const Bits& num_2)
{
    for(int i = 30; i >= 0; --i)
    {
        if(num_1.bits[i] ^ num_2.bits[i])
        {
            if(num_1.bits[i]) return 1;
            else return -1;
        }
    }
    return 0;
}

Bits::Bits(const int& num)
{
    if(num < 0) bits[31] = 1;
    int temp = fabs(num);
    int iter = 0;
    while(temp >= 1)
    {
        bits[iter++] = temp % 2;
        temp /= 2;
    }
}

Bits::Bits(const Bits& num_to_copy)
{
    for(int i = 0; i < 32; i++) this->bits[i] = num_to_copy.bits[i];
}

Bits Bits::to_floating_point_format()
{
    int size = this->size();
    *this << (22 - size);
    int temp = fabs(size + 1);
    int iter = 23;
    while(temp >= 1)
    {
        if(iter == 0) break;
        this->bits[iter++] = temp % 2;
        temp /= 2;
    }
    return *this;

}

Bits Bits::to_first_completion()
{
    if(bits[31] == 0) return *this;
    for(int i = 0; i < 31; ++i) bits[i] = ~bits[i];
    return *this;
}

Bits Bits::to_second_completion()
{
    if(bits[31] == 0) return *this;
    this->to_first_completion();
    Bits one(1);
    bool carry = 0;
    for(int i = 0; i < 32; ++i)
    {
        int temp = bits[i] + one.bits[i] + carry;
        bits[i] = temp % 2;
        carry = temp / 2;
    }
    return *this;
}

std::ostream& operator<<(std::ostream& output, const Bits& num)
{
    output << num.bits;
    return output;
}

Bits operator+(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    result = result.add_second_completion(num_1, num_2);
    return result;
}

Bits operator-(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    result = result.subtract_second_completion(num_1, num_2);
    return result;
}

Bits operator*(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    result = result.multiply(num_1, num_2);
    return result;
}

Bits operator/(const Bits& num_1, const Bits& num_2)
{
    Bits result;
    result = result.divide(num_1, num_2);
    return result;
}

bool operator==(const Bits& num_1, const Bits& num_2)
{
    for(int i = 0; i < 31; ++i) if(num_1.bits[i] ^ num_2.bits[i]) return false;
    return true;
}

Bits Bits::operator<<(const int& shift)
{
    for(int i = 30; i >= 0; --i) this->bits[i] = this->bits[i - shift];
    return *this;
}

Bits Bits::operator>>(const int& shift)
{
    for(int i = 0; i <= 30; i++) 
    {
        if((i + shift) > 30) this->bits[i] = 0;
        else this->bits[i] = this->bits[i + shift];
    }
    return *this;
}
