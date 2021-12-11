#include <stdio.h>
#include <stdlib.h>
#include "associative_processor.h"

bool function_1(bool a, bool b) { return a&b; }
bool function_14(bool a, bool b) { return !(a&b); }
bool function_3(bool a, bool b) { return a; }
bool function_12(bool a, bool b) { return !a; }

void fill_memory(word*);
void print_memory(word*);



int main()
{
    word* memory = create_diagonal_memory(SIZE_OF_MEMORY, WORD_SIZE);
    fill_memory(memory);
    print_memory(memory);

    // Read example
    printf("\nREADING_4th_WORD\n");
    word readed = read_from_diagonal_memory(memory, 4);
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", readed.digit[i]);

    // Write example
    printf("\nWRITE_WORD_NUMBER_0_TO_7_POS\n");
    write_to_diagonal_memory(memory, memory[0], 7);
    print_memory(memory);

    // Logical functions using example
    printf("\nFUNCTION_1(0, 1, 2): ");
    logical_operation_diagonal_memory(memory, 0, 1, 2, function_1);
    word answer = read_from_diagonal_memory(memory, 2);
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", answer.digit[i]);
    printf("\nFUNCTION_14(0, 1, 2): ");
    logical_operation_diagonal_memory(memory, 0, 1, 2, function_14);
    answer = read_from_diagonal_memory(memory, 2);
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", answer.digit[i]);
    printf("\n\nFUNCTION_3(0, 1, 2): ");
    logical_operation_diagonal_memory(memory, 0, 1, 2, function_3);
    answer = read_from_diagonal_memory(memory, 2);
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", answer.digit[i]);
    printf("\nFUNCTION_12(0, 1, 2): ");
    logical_operation_diagonal_memory(memory, 0, 1, 2, function_12);
    answer = read_from_diagonal_memory(memory, 2);
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", answer.digit[i]);
    printf("\n\n");

    // Searching nearest example
    printf("SEARCHING_NEAREST_UP:\n");
    word nearest = find_nearest(memory, memory[2], UP);
    printf("NESESSARY_ANSWER: 1010000111001010\n");
    printf("ACTUAL_ANSWER: ");
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", nearest.digit[i]);
    printf("\n\n");
    printf("SEARCHING_NEAREST_DOWN:\n");
    nearest = find_nearest(memory, memory[2], DOWN);
    printf("NESESSARY_ANSWER: 1010111110001010\n");
    printf("ACTUAL_ANSWER: ");
    for (int i = 0; i < WORD_SIZE; ++i) printf("%d", nearest.digit[i]);
    printf("\n\n");

    // Addiotion example
    printf("ADDITION (TEMPLATE: 110):\n");
    bool* example = (bool*)malloc(WORD_SIZE * sizeof(bool));
    example[13] = 1; example[14] = 1; example[15] = 0;
    addition(memory, example);
    print_memory(memory);
    free(example);
    free_diagonal_memory(memory);
    return 0;
}


void fill_memory(word* memory)
{
    for (int i = 0; i < SIZE_OF_MEMORY; ++i)
    {
        for (int j = 0; j < WORD_SIZE; ++j) memory[i].digit[j] = rand()%2;
    }
}

void print_memory(word* memory)
{
    for (int i = 0; i < SIZE_OF_MEMORY; ++i)
    {
        printf("[%d]\t", i);
        for (int j = 0; j < WORD_SIZE; ++j) printf("%d", memory[i].digit[j]);
        printf("\n");
    }
}
