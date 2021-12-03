#include <stdio.h>
#include "associative_processor.h"

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
    for (int i = 0; i < SIZE_OF_MEMORY; ++i) result_array[i].digit = NULL;
    int index = 0;
    if (direction == down)
    {
        for (int i = 0; i < SIZE_OF_MEMORY; ++i)
            if (compare_words(query, memory[i], 0).l) result_array[index++] = memory[i];
        word max = result_array[0];
        for (int i = 0; result_array[i].digit != NULL; ++i)
            if (compare_words(max, result_array[i], 0).g) max = result_array[i];
        nearest = max;
    }
    else
    {
        for (int i = 0; i < SIZE_OF_MEMORY; ++i)
            if (compare_words(query, memory[i], 0).g) result_array[index++] = memory[i];
        word min = result_array[0];
        for (int i = 0; result_array[i].digit != NULL; ++i)
            if (compare_words(min, result_array[i], 0).l) min = result_array[i];
        nearest = min;
    }
    return nearest;
}
