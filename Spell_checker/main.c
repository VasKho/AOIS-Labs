#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "spell_check.h"

int main(int argc, char* argv[])
{
    FILE* dictionary;
    if (argc > 1) dictionary = fopen(argv[1], "rb");
    else
    {
        printf("You should add dictionary file\n");
        printf("Usage example: ./main dictionary.txt\n");
        exit(1);
    }
    if (!dictionary)
    {
        printf("No such file or directory!\n");
        exit(1);
    }
    fseek(dictionary, 0L, SEEK_END);
    unsigned long size = ftell(dictionary);
    fseek(dictionary, 0L, SEEK_SET);
    trie_node* root = gen_node();
    char* word = (char*)malloc(sizeof(char)*size);
    while (!feof(dictionary))
    {
        fscanf(dictionary, "%s\n", word);
        insert(root, word);
    }

    char query[30];
    while(1)
    {
        scanf("%s", query);
        if (strcmp(query, "q") == 0) break;
        print_suggestions(root, query);
    }
    trie_free(root);
    return 0;
}
