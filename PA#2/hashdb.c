#include "hashdb.h"
#include "rwlocks.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// Jenkins's one-at-a-time hash function
uint32_t jenkins_one_at_a_time_hash(char *key, size_t len) {
    uint32_t hash = 0;
    for (size_t i = 0; i < len; i++) {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return hash;
}

// Initialize the hash table and lock
hashRecord *hashTable[256]; // Simplified size for demonstration
rwlock_t lock = NULL;
rwlock_init(&lock);

// Insert function with output
void insert(char *key, uint32_t salary, FILE *output) {
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    rwlock_acquire_writelock(&lock);
    hashRecord *prev = NULL;
    hashRecord *entry = hashTable[hash % 256];

    while (entry != NULL && strcmp(entry->name, key) != 0) {
        prev = entry;
        entry = entry->next;
    }

    if (entry == NULL) {
        entry = (hashRecord *)malloc(sizeof(hashRecord));
        entry->hash = hash;
        strcpy(entry->name, key);
        entry->salary = salary;
        entry->next = NULL;
        
        if (prev == NULL) {
            hashTable[hash % 256] = entry;
        } else {
            prev->next = entry;
        }
        fprintf(output, "%u, %s, %u\n", hash, key, salary);
    } else {
        // Update existing entry
        entry->salary = salary;
        fprintf(output, "%u, %s, %u\n", hash, key, salary);
    }
    rwlock_release_writelock(&lock);
}

// Delete function with output
void delete(char *key, FILE *output) {
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    rwlock_acquire_writelock(&lock);
    hashRecord *prev = NULL;
    hashRecord *entry = hashTable[hash % 256];

    while (entry != NULL && strcmp(entry->name, key) != 0) {
        prev = entry;
        entry = entry->next;
    }

    if (entry != NULL) {
        if (prev == NULL) {
            hashTable[hash % 256] = entry->next;
        } else {
            prev->next = entry->next;
        }
        fprintf(output, "%u, %s\n", hash, key);
        free(entry);
    } else {
        printf("Delete Attempted: Hash=%u, Name=%s (Not Found)\n", hash, key);
    }
    rwlock_release_writelock(&lock);
}

// Search function with output
uint32_t search(char *key, FILE *output) {
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    rwlock_acquire_readlock(&lock);
    hashRecord *entry = hashTable[hash % 256];

    while (entry != NULL) {
        if (strcmp(entry->name, key) == 0) {
            rwlock_release_readlock(&lock);
            fprintf(output, "%u, %s, %u\n", hash, key, entry->salary);
            return entry->salary;
        }
        entry = entry->next;
    }
    rwlock_release_readlock(&lock);
    printf("Search: Hash=%u, Name=%s (Not Found)\n", hash, key);
    return 0; // Assuming 0 is not a valid salary and indicates not found
}

void printTable(FILE *output) {
    rwlock_acquire_readlock(&lock);
    hashRecord *entry;
    for (int n = 0; n < 256; n++) {
        entry = hashTable[n];
        while (entry != NULL) {
            if (entry != NULL) fprintf(output, "%u, %s, %u\n", entry->hash, entry->name, entry->salary);
            entry = entry->next;
        }
    }
    rwlock_release_readlock(&lock);
}

// Example command processing
int main() {
    // Initialize hash table
    memset(hashTable, 0, sizeof(hashTable));
    
    // Process sample commands
    FILE *example = fopen("example.txt", "w");
    insert("John Doe", 45000);
    delete("John Doe");
    search("John Doe");

    return 0;
}
