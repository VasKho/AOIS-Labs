#include <stdio.h>
#include <string.h>
#include "spell_check.h"

int main()
{
    trie_node* root = gen_node();
    insert(root, "shot");
    insert(root, "shit");
    insert(root, "shift");
    insert(root, "tree");

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
