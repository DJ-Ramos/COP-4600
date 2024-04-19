#ifndef HASHDB_H
#define HASHDB_H

#include "rwlocks.h"
#include <stdint.h>
#include <pthread.h>

// Define the structure for hash records
typedef struct hash_struct {
    uint32_t hash;
    char name[50];
    uint32_t salary;
    struct hash_struct *next;
} hashRecord;

// Function prototypes
void insert(char *key, uint32_t salary);
void delete(char *key);
uint32_t search(char *key);
void print();

// Lock for concurrency control
rwlock_t lock;

#endif // HASHDB_H
