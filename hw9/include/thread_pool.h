#ifndef __THREAD_POOL_H__
#define __THREAD_POOL_H__

#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "wsqueue.h"

struct Task {
    struct list_node node;
    void (*f) (void *); 
    void *arg;
 
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    bool done;
};


struct ThreadPool {  
    int threads_nm;
    pthread_t *threads;
    struct wsqueue tasks;
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);

#endif
