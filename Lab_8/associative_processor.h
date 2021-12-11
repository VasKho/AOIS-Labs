#ifndef _ASSOCIATIVE_PROCESSOR_H_
#define _ASSOCIATIVE_PROCESSOR_H_
#include <stdbool.h>


#define SIZE_OF_MEMORY 16
#define WORD_SIZE 16

enum direction {UP = 0, DOWN = 1};


typedef struct word word;

struct word
{
    bool digit[WORD_SIZE];
    int number_of_elems;
};


typedef struct gl gl;

struct gl
{
	bool g;
	bool l;
};

word* create_diagonal_memory(int, int);
void free_diagonal_memory(word*);

gl compare_words(word, word, int); 
word find_nearest(word*, word, enum direction);

void write_to_diagonal_memory(word*, word, int);
word read_from_diagonal_memory(word*, int);

void logical_operation_diagonal_memory(word*, int, int, int, bool (*)(bool, bool));
void addition(word*, bool*);

#endif
