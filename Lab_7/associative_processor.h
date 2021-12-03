#ifndef _ASSOCIATIVE_PROCESSOR_H_
#define _ASSOCIATIVE_PROCESSOR_H_
#include <stdbool.h>


#define SIZE_OF_MEMORY 40
#define WORD_SIZE 10
#define SEARCH_ACCURACY 6

enum direction {up = 0, down = 1};


typedef struct word word;

struct word
{
    bool* digit;
};


typedef struct gl gl;

struct gl
{
	bool g;
	bool l;
};

gl compare_words(word, word, int); 
word find_nearest(word*, word, enum direction);

#endif
