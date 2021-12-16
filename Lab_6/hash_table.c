#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hash_table.h"
#include <math.h>


void hash_queue_push(hash_queue** queue, const char* key, const char* info)
{
    hash_queue* new_note = (hash_queue*)malloc(sizeof(hash_queue));
    new_note->key = (char*)malloc(strlen(key) * sizeof(char) + 1);
    new_note->value = (char*)malloc(strlen(info) * sizeof(char) + 1);
    strncpy(new_note->key, key, strlen(key));
    strncpy(new_note->value, info, strlen(info));
    if (*queue == NULL)
    {
        new_note->next = NULL;
        new_note->previous = NULL;
        *queue = new_note;
        return;
    }
    (*queue)->previous = new_note;
    new_note->next = *queue;
    *queue = new_note;
}

void hash_queue_pop(hash_queue** queue)
{
    if (*queue == NULL) return;
    hash_queue* temp = (*queue)->next;
    free((*queue)->key);
    free((*queue)->value);
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
            else 
            {
                if (del->next == NULL)
                {
                    free(del->key);
                    free(del->value);
                    free(del);
                    *queue = NULL;
                    return;
                }
                del->next->previous = NULL;
                *queue = del->next;
            }
            if (del->next != NULL) del->next->previous = del->previous;
            else del->previous->next = NULL;
            free(del->key);
            free(del->value);
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
    printf("\"%s\" no such element in queue", key);
    return "";
}

void hash_queue_free(hash_queue** queue)
{
    while(*queue != NULL) hash_queue_pop(queue);
}


hash_table* hash_table_create(int size)
{
    hash_table* table = (hash_table*)malloc(size * sizeof(hash_table));
    for(int i = 0; i < size; ++i)
    {
        table[i].key = NULL;
        table[i].value = NULL;
        table[i].size = size;
        table[i].same_hash_list = NULL;
    }
    return table;
}

void hash_table_free(hash_table* table)
{
    hash_table* temp_table = table;
    for (int i = 0; i < temp_table->size; ++i)
    {
        if (temp_table[i].same_hash_list != NULL) hash_queue_free(&temp_table[i].same_hash_list);
        if (temp_table[i].key != NULL) free(temp_table[i].key);
        if (temp_table[i].value != NULL) free(temp_table[i].value);
    }
    free(table);
}

void hash_table_insert(hash_table* table, const char* key, char* info)
{
    unsigned long curr_hash = get_hash(key); 
    int position = curr_hash % table->size;
    if (table[position].key == NULL)
    {
        table[position].key = (char*)malloc(strlen(key) * sizeof(char) + 1);
        table[position].value = (char*)malloc(strlen(info) * sizeof(char) + 1);
        strncpy(table[position].key, key, strlen(key));
        strncpy(table[position].value, info, strlen(key));
    }
    else
    {
        if (strcmp(table[position].key, key) == 0)
        {
            printf("\"%s\" key already exists in hash table\n", key);
            exit(1);
        }
        hash_queue_push(&table[position].same_hash_list, key, info);
    }
}

void hash_table_delete(hash_table* table, const char* key)
{
    int position = get_hash(key) % table->size;
    if (table[position].same_hash_list == NULL) 
    {
        free(table[position].key);
        table[position].key = NULL;
        free(table[position].value);
        table[position].value = NULL;
    }
    else
    {
        if (strcmp(table[position].key, key) == 0)
        {
            table[position].key = table[position].same_hash_list->key;
            table[position].value = table[position].same_hash_list->value;
            hash_queue_pop(&table[position].same_hash_list);
        }
        else hash_queue_delete(&table[position].same_hash_list, key);
    }
}

char* hash_table_find(hash_table* table, const char* key)
{
    int position = get_hash(key) % table->size;
    if (position >= table->size)
    {
        printf("\"%s\" no such element in hash table", key);
        return "";
    }
    if (table[position].key != NULL && strcmp(table[position].key, key) == 0) return table[position].value;
    if (table[position].same_hash_list == NULL)
    {
        printf("\"%s\" no such element in hash table", key);
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
