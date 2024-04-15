// Reader-Writer lock struct definitions
#ifndef READ_WRITE_LOCKS_HEADER_FILE
#define READ_WRITE_LOCKS_HEADER_FILE

#include <semaphore.h>

typedef struct rwlock_t
{
    sem_t writelock;
    sem_t lock;
    int readers;
} rwlock_t;

void rwlock_init(rwlock_t *lock);
void rwlock_acquire_readlock(rwlock_t *lock);
void rwlock_release_readlock(rwlock_t *lock);
void rwlock_acquire_writelock(rwlock_t *lock);
void rwlock_release_writelock(rwlock_t *lock);

#endif