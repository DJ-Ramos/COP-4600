#ifndef HASHDB_H
#define HASHDB_H

#include "rwlocks.h"
#include <stdint.h>
#include <pthread.h>
#include <stdio.h>

typedef struct hash_struct
{
    uint32_t hash;
    char name[50];
    uint32_t salary;
    struct hash_struct *next;
} hashRecord;

extern FILE *outputFile;
// rwlock_t lock; 

void insert(char *key, uint32_t salary);
void delete(char *key);
hashRecord *search(char *key);
void print();
hashRecord *sortRecords(unsigned short records);

#endif // HASHDB_H
