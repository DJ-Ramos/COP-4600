#ifndef HASHDB_H
#define HASHDB_H

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
void insert(char *key, uint32_t salary, FILE *output);
void delete(char *key, FILE *output);
uint32_t search(char *key, FILE *output);
void print(FILE *output);

// Lock for concurrency control
pthread_rwlock_t lock;

#endif // HASHDB_H
