#include <stdio.h>
#include <stdint.h>
#include <string.h>

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

int main() {
    char key[] = "Shigeru Miyamoto";
    uint32_t hash = jenkins_one_at_a_time_hash(key, strlen(key));
    printf("\nHash for '%s' is %u\n", key, hash);
    return 0;
}