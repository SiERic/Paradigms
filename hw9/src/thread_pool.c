#include "thread_pool.h"

static void *thpool_work(void *_pool) {
    struct ThreadPool *pool = _pool;
    while (1) {
        wsqueue_wait(&(pool->tasks));
        struct Task *task = (struct Task*)(wsqueue_pop(&(pool->tasks)));
        if (!task) continue;
        if (!task->f) break;
        task->f(task->arg);
        pthread_mutex_lock(&(task->mutex));
        task->done = 1;
        pthread_cond_signal(&(task->cond));
        pthread_mutex_unlock(&(task->mutex));
    } 
    return 0;
}


void thpool_init(struct ThreadPool* pool, unsigned threads_nm) {
    pool->threads_nm = threads_nm;
    pool->threads = malloc(threads_nm * sizeof(pthread_t));
    wsqueue_init(&(pool->tasks));
    for (int i = 0; i < (int)threads_nm; ++i) {
        pthread_create(&(pool->threads[i]), NULL, thpool_work, pool);
    }
}
 
void thpool_submit(struct ThreadPool *pool, struct Task *task) {
    pthread_mutex_init(&(task->mutex), NULL);
    pthread_cond_init(&(task->cond), NULL);
    task->done = 0;

    wsqueue_push(&(pool->tasks), &(task->node));
}



void thpool_wait(struct Task* task) {
    pthread_mutex_lock(&(task->mutex));
    while (!task->done) {
        pthread_cond_wait(&(task->cond), &(task->mutex));
    }
    pthread_mutex_unlock(&(task->mutex));
}


void thpool_finit(struct ThreadPool* pool) {
    struct Task *finit_tasks = malloc(sizeof(struct Task) * pool->threads_nm);
    
    for (int i = 0; i < (int)pool->threads_nm; i++){
        finit_tasks[i].f = NULL;
        thpool_submit(pool, &finit_tasks[i]);
    }

    for (int i = 0; i < (int)pool->threads_nm; i++){
        pthread_join(pool->threads[i], NULL);
    }
    free(pool->threads);
    free(finit_tasks);
    wsqueue_finit(&pool->tasks);
}
