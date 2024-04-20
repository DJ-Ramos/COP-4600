#include "hashdb.h"
#include "rwlocks.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

uint32_t jenkins_one_at_a_time_hash(char *key, size_t len)
{
    uint32_t hash = 0;
    for (size_t i = 0; i < len; i++)
    {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return hash;
}

hashRecord *hashTable;

void insert(char *key, uint32_t salary)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    fprintf(outputFile,"INSERT,%u,%s,%u\n", hash, key, salary);
    rwlock_acquire_writelock(&lock);
    hashRecord *prev = NULL;
    hashRecord *record = hashTable;

    while (record != NULL && strcmp(record->name, key) != 0)
    {
        prev = record;
        record = record->next;
    }

    if (record == NULL)
    {
        record = (hashRecord *)malloc(sizeof(hashRecord));
        record->hash = hash;
        strcpy(record->name, key);
        record->salary = salary;
        record->next = NULL;

        if (prev == NULL)
        {
            hashTable = record;
        }
        else
        {
            prev->next = record;
        }
    }
    else
    {
        record->salary = salary;
    }
    rwlock_release_writelock(&lock);
}

void delete(char *key)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    fprintf(outputFile,"DELETE,%s\n", key);
    rwlock_acquire_writelock(&lock);
    hashRecord *prev = NULL;
    hashRecord *record = hashTable;

    while (record != NULL && strcmp(record->name, key) != 0)
    {
        prev = record;
        record = record->next;
    }

    if (record != NULL)
    {
        if (prev == NULL)
        {
            hashTable = record->next;
        }
        else
        {
            prev->next = record->next;
        }
        free(record);
    }
    rwlock_release_writelock(&lock);
}

hashRecord *search(char *key)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    fprintf(outputFile,"SEARCH,%s\n", key);
    rwlock_acquire_readlock(&lock);
    hashRecord *record = hashTable;

    while (record != NULL)
    {
        if (strcmp(record->name, key) == 0)
        {
            rwlock_release_readlock(&lock);
            return record;
        }
        record = record->next;
    }
    rwlock_release_readlock(&lock);
    return NULL;
}

void print()
{
    rwlock_acquire_readlock(&lock);
    hashRecord *record = hashTable;
    while (record != NULL)
    {
        fprintf(outputFile,"%u,%s,%u\n", record->hash, record->name, record->salary);
        record = record->next;
    }
    rwlock_release_readlock(&lock);
}

hashRecord *sortRecords(unsigned short records)
{
    rwlock_acquire_readlock(&lock);
    hashRecord *record = hashTable;
    hashRecord *temp = NULL;

    for (int i = 0; i < records - 1; i++)
    {
        for (int j = i + 1; j < records; j++)
        {
            if (record->hash > record->next->hash)
            {
                temp = record;
                record = record->next;
                record->next = temp;

            }
        }
    }

    rwlock_release_readlock(&lock);
    return hashTable;
}
