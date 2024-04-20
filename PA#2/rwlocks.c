#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <semaphore.h>

#include "common.h"
#include "common_threads.h"
#include "rwlocks.h"
#include "hashdb.h"

void rwlock_init(rwlock_t *lock)
{
    lock->readers = 0;
    sem_init(&lock->lock, 0, 1);
    sem_init(&lock->writelock, 0, 1);
}

void rwlock_acquire_readlock(rwlock_t *lock)
{
    sem_wait(&lock->lock);
    fprintf(outputFile,"READ LOCK ACQUIRED\n");
    lock->readers++;
    if (lock->readers == 1)
        sem_wait(&lock->writelock);
    sem_post(&lock->lock);
}

void rwlock_release_readlock(rwlock_t *lock)
{
    sem_wait(&lock->lock);
    fprintf(outputFile,"READ LOCK RELEASED\n");
    lock->readers--;
    if (lock->readers == 0)
        sem_post(&lock->writelock);
    sem_post(&lock->lock);
}

void rwlock_acquire_writelock(rwlock_t *lock)
{
    sem_wait(&lock->writelock);
    fprintf(outputFile,"WRITE LOCK ACQUIRED\n");
}

void rwlock_release_writelock(rwlock_t *lock)
{
    sem_post(&lock->writelock);
    fprintf(outputFile,"WRITE LOCK RELEASED\n");
}
