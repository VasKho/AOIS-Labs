#include <malloc.h>
#include <string.h>
#include <stdlib.h>
#include "hash_table.h"


void hash_queue_push_front(hash_queue** queue, const char* key, char* info)
{
    hash_queue* new_note = (hash_queue*)malloc(sizeof(hash_queue));
    new_note->key = (char*)malloc(strlen(key) * sizeof(*key));
    new_note->value = (char*)malloc(strlen(info) * sizeof(*info));
    strcpy(new_note->key, key);
    strcpy(new_note->value, info);
    if (*queue == NULL)
    {
        *queue = new_note;
        (*queue)->next = NULL;
        (*queue)->previous = NULL;
        return;
    }
    (*queue)->next = new_note;
    new_note->previous = *queue;
}

void hash_queue_pop_front(hash_queue** queue)
{
    if (*queue == NULL) return;
    hash_queue* temp = (*queue)->previous;
    free((*queue));
    (*queue) = temp;
}

void hash_queue_delete(hash_queue** queue, const char* key)
{
    hash_queue* del = *queue;
    while(del != NULL)
    {
        if (strcmp(del->key, key) == 0)
        {
            if (del->previous != NULL) del->previous->next = del->next;
            else *queue = del->next;
            if (del->next != NULL) del->next->previous = del->previous;
            free(del);
            return;
        }
        del = del->next;
    }

}

char* hash_queue_find(hash_queue* queue, const char* key)
{
    hash_queue* temp = queue;
    while(temp != NULL)
    {
        if (strcmp(temp->key, key) == 0) return temp->value;
        temp = temp->next;
    }
    printf("No such element in queue");
    return "";
}


hash_table* hash_table_create(int size)
{
    hash_table* table = (hash_table*)malloc(size * sizeof(hash_table));
    for(int i = 0; i < size; ++i)
    {
        table[i].key = "";
        table[i].value = NULL;
        table[i].size = size;
        table[i].same_hash_list = NULL;
    }
    return table;
}

void hash_table_destroy(hash_table* table)
{
    free(table);
}

void hash_table_insert(hash_table* table, const char* key, char* info)
{
    unsigned long curr_hash = get_hash(key); 
    int position = curr_hash % table->size;
    if (strcmp(table[position].key, "") == 0)
    {
        table[position].key = (char*)malloc(strlen(key) * sizeof(*key));
        table[position].value = (char*)malloc(strlen(info) * sizeof(*info));
        strcpy(table[position].key, key);
        strcpy(table[position].value, info);
    }
    else
    {
        if (strcmp(table[position].key, key) == 0)
        {
            printf("\"%s\" key already exists in hash table\n", key);
            exit(1);
        }
        hash_queue_push_front(&table[position].same_hash_list, key, info);
    }
}

void hash_table_delete(hash_table* table, const char* key)
{
    int position = get_hash(key) % table->size;
    if (table[position].same_hash_list == NULL) 
    {
        free(table[position].key);
        table[position].key = "";
        free(table[position].value);
        table[position].value = NULL;
    }
    else
    {
        if (strcmp(table[position].key, key) == 0)
        {
            table[position].key = table[position].same_hash_list->key;
            table[position].value = table[position].same_hash_list->value;
            hash_queue_pop_front(&table[position].same_hash_list);
        }
        else hash_queue_delete(&table[position].same_hash_list, key);
    }
}

char* hash_table_find(hash_table* table, const char* key)
{
    int position = get_hash(key) % table->size;
    if (position >= table->size)
    {
        printf("No such element in hash table");
        return "";
    }
    if (strcmp(table[position].key, key) == 0) return table[position].value;
    if (table[position].same_hash_list == NULL)
    {
        printf("No such element in hash table");
        return "";
    }
    return hash_queue_find(table[position].same_hash_list, key);
}

unsigned long get_hash(const char* key)
{
    unsigned long hash = 0;
    for(int i = 0; *(key + i) != '\0'; ++i) hash ^= *(key + i);
    return hash;
}
