#include "hashdb.h"
#include "rwlocks.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// Jenkins's one-at-a-time hash function
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

// Insert function with output
void insert(char *key, uint32_t salary)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    printf("INSERT,%u,%s,%u\n", hash, key, salary);
    rwlock_acquire_writelock(&lock);
    printf("\n");
    hashRecord *prev = NULL;
    hashRecord *entry = hashTable;

    while (entry != NULL && strcmp(entry->name, key) != 0)
    {
        prev = entry;
        entry = entry->next;
    }

    if (entry == NULL)
    {
        entry = (hashRecord *)malloc(sizeof(hashRecord));
        entry->hash = hash;
        strcpy(entry->name, key);
        entry->salary = salary;
        entry->next = NULL;

        if (prev == NULL)
        {
            hashTable = entry;
        }
        else
        {
            prev->next = entry;
        }
    }
    else
    {
        // Update existing entry
        entry->salary = salary;
    }
    rwlock_release_writelock(&lock);
    printf("\n");
}

// Delete function with output
void delete(char *key)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    printf("DELETE,%s\n", key);
    rwlock_acquire_writelock(&lock);
    printf("\n");
    hashRecord *prev = NULL;
    hashRecord *entry = hashTable;

    while (entry != NULL && strcmp(entry->name, key) != 0)
    {
        prev = entry;
        entry = entry->next;
    }

    if (entry != NULL)
    {
        if (prev == NULL)
        {
            hashTable = entry->next;
        }
        else
        {
            prev->next = entry->next;
        }
        free(entry);
    }
    rwlock_release_writelock(&lock);
    printf("\n");
}

// Search function with output
uint32_t search(char *key)
{
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    printf("SEARCH,%s\n", key);
    rwlock_acquire_readlock(&lock);
    printf("\n");
    hashRecord *entry = hashTable;


    while (entry != NULL)
    {
        if (strcmp(entry->name, key) == 0)
        {
            rwlock_release_readlock(&lock);
            return entry->hash;
        }
        entry = entry->next;
    }
    rwlock_release_readlock(&lock);
    printf("\n");
    return 0;
}

void print()
{
    rwlock_acquire_readlock(&lock);
    printf("\n");
    rwlock_release_readlock(&lock);
    printf("\n");
}
