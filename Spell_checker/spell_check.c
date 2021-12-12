#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include "spell_check.h"
 

trie_node* gen_node()
{
    trie_node* new_node = (trie_node*)malloc(sizeof(trie_node));
 
    if (new_node)
    {
        new_node->is_end_of_word = false;
        for (int i = 0; i < ALPHABET_SIZE; ++i) new_node->children[i] = NULL;
    }
    return new_node;
}
 

void insert(trie_node* root, const char* key)
{
    int length = strlen(key);
    int index;
 
    trie_node *cur_pos_ptr = root;
 
    for (int level = 0; level < length; ++level)
    {
        index = CHAR_TO_INDEX(key[level]);
        if (!cur_pos_ptr->children[index])
            cur_pos_ptr->children[index] = gen_node();
 
        cur_pos_ptr = cur_pos_ptr->children[index];
    }
    cur_pos_ptr->is_end_of_word = true;
}


bool search(trie_node* root, const char* key)
{
    int length = strlen(key);
    int index;
    trie_node* cur_pos_ptr = root;
 
    for (int level = 0; level < length; level++)
    {
        index = CHAR_TO_INDEX(key[level]);
 
        if (!cur_pos_ptr->children[index]) return false;
        cur_pos_ptr = cur_pos_ptr->children[index];
    }
 
    return cur_pos_ptr->is_end_of_word;
}


void find_variants_of_match(trie_node* root, const char* res)
{
    if (root->is_end_of_word == true) printf("%s\n", res);
 
    for (int i = 0; i < ALPHABET_SIZE; ++i)
    {
        if (root->children[i] != NULL)
        {
            char* new_suggestion = (char*)malloc((strlen(res) + 2) * sizeof(char));
            strcpy(new_suggestion, res);
            char new_letter = i + 'a';
            strncat(new_suggestion, &new_letter, 1);
            find_variants_of_match(root->children[i], new_suggestion);
            free(new_suggestion);
        }
    }
}


void print_suggestions(trie_node* root, const char* res)
{
    int length = strlen(res);
    int index;
    trie_node* cur_pos_ptr = root;

    if (!cur_pos_ptr->children[CHAR_TO_INDEX(res[0])]) return;

    for(int level = 0; level < length; ++level)
    {
        index = CHAR_TO_INDEX(res[level]);

        if (!cur_pos_ptr->children[index]) break;
        cur_pos_ptr = cur_pos_ptr->children[index];
    }
    find_variants_of_match(cur_pos_ptr, res);
}


void trie_free(trie_node* root)
{
    if (root->is_end_of_word)
    {
        free(root);
        return;
    }

    trie_node* cur_pos_ptr = root;

    for(int i = 0; i < ALPHABET_SIZE; ++i)
        if (cur_pos_ptr->children[i] != NULL)
            trie_free(cur_pos_ptr->children[i]);

    free(cur_pos_ptr);
}
