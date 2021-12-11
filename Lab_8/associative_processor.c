#include <stdio.h>
#include <stdlib.h>
#include "associative_processor.h"


word* create_diagonal_memory(int number_of_words, int number_of_digits)
{
    word* memory = (word*)malloc(number_of_words * sizeof(word));
    memory->number_of_elems = number_of_words;
    for (int i = 0; i < number_of_words; ++i)
        memory[i].number_of_elems = number_of_digits;
    return memory;
}


void free_diagonal_memory(word* memory)
{
    free(memory);
}


// This function recursively compare two words in memory
// output - struct gl
// i.e.
// (l = 0, g = 0) => input_word == word_from_storage
// (l = 1, g = 0) => input_word > word_from_storage
// (l = 0, g = 1) => input_word < word_from_storage
gl compare_words(word input_word, word word_from_storage, int digit)
{
    gl current, next;
    if (digit + 1 == WORD_SIZE)
    {
        next.g = false;
        next.l = false;
    }
    else next = compare_words(input_word, word_from_storage, digit + 1); 
    current.g = next.g | (!input_word.digit[digit] & word_from_storage.digit[digit] & !next.l);
    current.l = next.l | (input_word.digit[digit] & !word_from_storage.digit[digit] & !next.g);
    return current;
}


word find_nearest(word* memory, word query, enum direction direction)
{
    word nearest;
    word result_array[SIZE_OF_MEMORY];
    int index = 0;
    if (direction == DOWN)
    {
        for (int i = 0; i < SIZE_OF_MEMORY; ++i)
        {
            word some_word = read_from_diagonal_memory(memory, i);
            if (compare_words(query, some_word, 0).l) result_array[index++] = some_word;
        }
        word max = result_array[0];
        for (int i = 0; i < index; ++i)
            if (compare_words(max, result_array[i], 0).g) max = result_array[i];
        nearest = max;
    }
    else
    {
        for (int i = 0; i < SIZE_OF_MEMORY; ++i)
        {
            word some_word = read_from_diagonal_memory(memory, i);
            if (compare_words(query, some_word, 0).g) result_array[index++] = some_word;
        }
        word min = result_array[0];
        for (int i = 0; i < index; ++i)
            if (compare_words(min, result_array[i], 0).l) min = result_array[i];
        nearest = min;
    }
    return nearest;
}


word to_diagonal_address(word orig_address, int col_number)
{
    bool buffer_elem = orig_address.digit[orig_address.number_of_elems - 1];
    for (int i = 0; i < col_number; ++i)
    {
        buffer_elem = orig_address.digit[orig_address.number_of_elems - 1];
        for (int j = orig_address.number_of_elems - 1; j > 0 ; --j)
            orig_address.digit[j] = orig_address.digit[j - 1];
        orig_address.digit[0] = buffer_elem;
    }
    return orig_address;
}


void write_to_diagonal_memory(word* memory, word new_word, int col_number)
{
    new_word = to_diagonal_address(new_word, col_number);
    for (int i = 0; i < WORD_SIZE; ++i)
        memory[col_number].digit[i] = new_word.digit[i];
}


word read_from_diagonal_memory(word* memory, int col_number)
{
    word readed_word = memory[col_number];
    bool buffer_elem = readed_word.digit[0];
    for (int i = 0; i < col_number; ++i)
    {
        buffer_elem = readed_word.digit[0];
        for (int j = 0; j < readed_word.number_of_elems - 1; ++j)
            readed_word.digit[j] = readed_word.digit[j + 1];
        readed_word.digit[readed_word.number_of_elems - 1] = buffer_elem;
    }
    return readed_word;
}


void logical_operation_diagonal_memory(word* memory, int first_operand_pos, int second_operand_pos, int destination_pos, bool (*predicate)(bool, bool))
{
    word first_operand = read_from_diagonal_memory(memory, first_operand_pos);
    word second_operand = read_from_diagonal_memory(memory, second_operand_pos);
    word result = read_from_diagonal_memory(memory, destination_pos);
    for (int i = 0; i < WORD_SIZE; ++i)
        result.digit[i] = predicate(first_operand.digit[i], second_operand.digit[i]);
    write_to_diagonal_memory(memory, result, destination_pos);
}


word set_mask(word* memory, int pos_in_storage, int bits_to_show)
{
    word readed_word = read_from_diagonal_memory(memory, pos_in_storage);
    word mask;
    for (int i = 0; i < WORD_SIZE; ++i)
    {
        if (i < (WORD_SIZE - bits_to_show)) mask.digit[i] = 0;
        else mask.digit[i] = 1;
    }

    for (int i = 0; i < WORD_SIZE; ++i)
        readed_word.digit[i] = mask.digit[i] & readed_word.digit[i];

    return readed_word;
}


void addition(word* memory, bool* search)
{
    word search_query;
    for (int i = WORD_SIZE - 1; i >= 0; --i)
        search_query.digit[i] = search[i];
    word masked;
    for (int i = 0; i < SIZE_OF_MEMORY; ++i)
    {
        masked = set_mask(memory, i, 3);
        gl res = compare_words(search_query, masked, 0);
        if(!res.l && !res.g)
        {
            word nesessary_word = read_from_diagonal_memory(memory, i);
            bool carry = 0;
            for (int j = 0; j < 4; ++j)
            {
                nesessary_word.digit[j] = (nesessary_word.digit[j + 5] ^ nesessary_word.digit[j + 9]) ^ carry;
                carry = (nesessary_word.digit[j + 5] & carry) | (nesessary_word.digit[j + 9] & carry) | (nesessary_word.digit[j + 5] & nesessary_word.digit[j + 9]);
            }
            nesessary_word.digit[4] = carry;
            write_to_diagonal_memory(memory, nesessary_word, i);
        }
    }
}
