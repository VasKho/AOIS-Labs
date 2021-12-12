#ifndef _SPELL_CHECK_H_
#define _SPELL_CHECK_H_
#include <stdbool.h>


#define ALPHABET_SIZE (26)
#define CHAR_TO_INDEX(c) ((int)c - (int)'a')


typedef struct trie_node trie_node;

struct trie_node
{
    trie_node* children[ALPHABET_SIZE];
    bool is_end_of_word;
};


trie_node* gen_node();
void insert(trie_node*, const char*);
bool search(trie_node*, const char*);
void print_suggestions(trie_node*, const char*);
void trie_free(trie_node*);

#endif
