#ifndef _HASH_TABLE_H_
#define _HASH_TABLE_H_


typedef struct hash_queue hash_queue;

struct hash_queue
{
    char* key;
    char* value;
    hash_queue* next;
    hash_queue* previous;
};

void hash_queue_push_front(hash_queue**, const char*, char*);
void hash_queue_pop_front(hash_queue**);
void hash_queue_delete(hash_queue**, const char*);
char* hash_queue_find(hash_queue*, const char*);


typedef struct hash_table hash_table;

struct hash_table
{
    char* key;
    char* value;
    hash_queue* same_hash_list;
    int size;
};


hash_table* hash_table_create(int);
void hash_table_destroy(hash_table*);
void hash_table_insert(hash_table*, const char*, char*);
void hash_table_delete(hash_table*, const char*);
char* hash_table_find(hash_table*, const char*);

unsigned long get_hash(const char*);
#endif
