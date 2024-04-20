#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <semaphore.h>

#include "common.h"
#include "common_threads.h"
#include "rwlocks.h"

// Initializes a lock struct.
// Sets lock.readers to be 0 and initializes the two semaphores in the lock.
void rwlock_init(rwlock_t *lock)
{
    lock->readers = 0;
    // The second argument is set to 0 in sem_init, which means the semaphore is shared between threads in the same process.
    // The third argument (value) is 1, the reason is shown in the following function definitions
    sem_init(&lock->lock, 0, 1);
    sem_init(&lock->writelock, 0, 1);
}

void rwlock_acquire_readlock(rwlock_t *lock)
{
    // sem_wait decrements the value by 1. If the value is negative, the function waits until it is 0
    // this is locking the semaphore
    sem_wait(&lock->lock);
    printf("READ LOCK ACQUIRED");
    lock->readers++;
    if (lock->readers == 1)
        // multiple threads can read at the same time, but only one thread can write
        sem_wait(&lock->writelock);
    // unlock the semaphore here (increment value and wake up a thread)
    sem_post(&lock->lock);
}

void rwlock_release_readlock(rwlock_t *lock)
{
    sem_wait(&lock->lock);
    printf("READ LOCK RELEASED");
    lock->readers--;
    if (lock->readers == 0)
        sem_post(&lock->writelock);
    sem_post(&lock->lock);
}

void rwlock_acquire_writelock(rwlock_t *lock)
{
    sem_wait(&lock->writelock);
    printf("WRITE LOCK ACQUIRED");
}

void rwlock_release_writelock(rwlock_t *lock)
{
    sem_post(&lock->writelock);
    printf("WRITE LOCK RELEASED");
}

int read_loops;
int write_loops;
int counter = 0;

rwlock_t mutex;

void *reader(void *arg)
{
    int i;
    int local = 0;
    for (i = 0; i < read_loops; i++)
    {
        rwlock_acquire_readlock(&mutex);
        local = counter;
        rwlock_release_readlock(&mutex);
        printf("read %d\n", local);
    }
    printf("read done: %d\n", local);
    return NULL;
}

void *writer(void *arg)
{
    int i;
    for (i = 0; i < write_loops; i++)
    {
        rwlock_acquire_writelock(&mutex);
        counter++;
        rwlock_release_writelock(&mutex);
    }
    printf("write done\n");
    return NULL;
}
/*
int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "usage: rwlock readloops writeloops\n");
        exit(1);
    }
    read_loops = atoi(argv[1]);
    write_loops = atoi(argv[2]);

    rwlock_init(&mutex);
    pthread_t c1, c2;
    Pthread_create(&c1, NULL, reader, NULL);
    Pthread_create(&c2, NULL, writer, NULL);
    Pthread_join(c1, NULL);
    Pthread_join(c2, NULL);
    printf("all done\n");
    return 0;
}
*/