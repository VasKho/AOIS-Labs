#include "bits.hpp"

int main()
{
    Bits num_1(13);
    Bits num_2(26);
    Bits num_1_neg(-13);
    Bits num_2_neg(-26);
    std::cout << "ADDITION" <<std::endl;
    printf("\n");
    std::cout << "13 + 26" << std::endl;
    std::cout << "Direct: " << num_1.add(num_2) << std::endl;
    std::cout << "First completion: " << num_1.add_first_completion(num_2) << std::endl;
    std::cout << "Second completion: " << num_1.add_second_completion(num_2) << std::endl;
    printf("\n");

    num_1 = 13;
    num_2 = 26;
    num_1_neg = -13;
    num_2_neg = -26;

    std::cout << "13 - 26" << std::endl;
    std::cout << "Direct: " << num_1.add(num_2_neg) << std::endl;
    std::cout << "First completion: " << (num_1.add_first_completion(num_2_neg)).to_first_completion() << std::endl;
    std::cout << "Second completion: " << (num_1.add_second_completion(num_2_neg)).to_second_completion() << std::endl;
    printf("\n");

    num_1 = 13;
    num_2 = 26;
    num_1_neg = -13;
    num_2_neg = -26;

    std::cout << "-13 + 26" << std::endl;
    std::cout << "Direct: " << num_1_neg.add(num_2) << std::endl;
    std::cout << "First completion: " << (num_1_neg.add_first_completion(num_2)).to_first_completion() << std::endl;
    num_1_neg = -13;
    std::cout << "Second completion: " << (num_1_neg.add_second_completion(num_2)).to_second_completion() << std::endl;
    printf("\n");

    num_1 = 13;
    num_2 = 26;
    num_1_neg = -13;
    num_2_neg = -26;

    std::cout << "-13 + (-26)" << std::endl;
    std::cout << "Direct: " << num_1_neg.add(num_2_neg) << std::endl;
    std::cout << "First completion: " << (num_1_neg.add_first_completion(num_2_neg)).to_first_completion() << std::endl;
    num_1_neg = -13;
    num_2_neg = -26;
    std::cout << "Second completion: " << (num_1_neg.add_second_completion(num_2_neg)).to_second_completion() << std::endl;
    printf("\n");

    num_1 = 13;
    num_2 = 26;
    num_1_neg = -13;
    num_2_neg = -26;

    std::cout << "MULTIPLICATION" << std::endl;
    printf("\n");
    std::cout << "13 * 26" << std::endl;
    std::cout << num_1.multiply(num_2) << std::endl;
    printf("\n");

    std::cout << "-13 * 26" << std::endl;
    std::cout << num_1_neg.multiply(num_2) << std::endl;
    printf("\n");

    std::cout << "13 * (-26)" << std::endl;
    std::cout << num_1.multiply(num_2_neg) << std::endl;
    printf("\n");

    std::cout << "-13 * (-26)" << std::endl;
    std::cout << num_1_neg.multiply(num_2_neg) << std::endl;
    printf("\n");

    std::cout << "DIVISION" << std::endl;
    printf("\n");
    std::cout << "13 / 26" << std::endl;
    std::cout << num_1.divide(num_2) << std::endl;
    printf("\n");

    std::cout << "-13 / 26" << std::endl;
    std::cout << num_1_neg.divide(num_2) << std::endl;
    printf("\n");

    std::cout << "13 / (-26)" << std::endl;
    std::cout << num_1.divide(num_2_neg) << std::endl;
    printf("\n");

    std::cout << "-13 / (-26)" << std::endl;
    std::cout << num_1_neg.divide(num_2_neg) << std::endl;
    printf("\n");

    Bits fp_1(130000);
    Bits fp_2(2600000);

    fp_1.to_floating_point_format();
    fp_2.to_floating_point_format();

    std::cout << "ADDITION IN FP FORMAT" << std::endl;
    printf("\n");

    std::cout << fp_1.FP_sum(fp_2) << std::endl;
    return 0;
}
