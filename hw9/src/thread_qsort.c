#include "thread_qsort.h"

void swap(int *a, int *b) {
    int c = *a;
    *a = *b;
    *b = c;
}

int cmp(const void *a, const void *b) {
    return *((int*) a) - *((int*) b);
}

void thqsort_real_sort(void *_arg) {
    struct TaskArg *arg = _arg;

    if (arg->sz <= 1) return;
    
    if (arg->depth == 0) {
        qsort(arg->a, arg->sz, sizeof(int), cmp);
        return;
    }

    //Partition

    int x = arg->a[(rand() % arg->sz)];
    int i = 0, j = arg->sz - 1;
    while (i <= j) {
        while (arg->a[i] < x) i++;
        while (arg->a[j] > x) j--;
        if (i <= j) swap(&(arg->a[i++]), &(arg->a[j--]));
    }

    //Create new tasks

    struct Task *taskl = malloc(sizeof(struct Task));
    taskl->f = thqsort_real_sort;

    struct TaskArg *argl = malloc(sizeof(struct TaskArg));
    argl->a = arg->a;
    argl->sz = j + 1;
    argl->depth = arg->depth - 1;
    argl->pool = arg->pool;
    argl->left = NULL;
    argl->right = NULL;

    taskl->arg = argl;

    ((struct TaskArg*)(_arg))->left = taskl;


    struct Task *taskr = malloc(sizeof(struct Task));
    taskr->f = thqsort_real_sort;

    struct TaskArg *argr = malloc(sizeof(struct TaskArg));
    argr->a = arg->a + i;
    argr->sz = arg->sz - i;
    argr->depth = arg->depth - 1;
    argr->pool = arg->pool;
    argr->left = NULL;
    argr->right = NULL;

    taskr->arg = argr;

    ((struct TaskArg*)(_arg))->right = taskr;


    thpool_submit(arg->pool, taskl);
    thpool_submit(arg->pool, taskr);
}

void wait_for_all_tasks(struct Task *task) {
    if (!task) return;
    if (!task->done) thpool_wait(task);
    wait_for_all_tasks(((struct TaskArg*)(task->arg))->left);
    wait_for_all_tasks(((struct TaskArg*)(task->arg))->right);
    free(task->arg);
    free(task);
}

void thqsort(int *a, int sz, int nTh, int depth) {
    struct ThreadPool pool;
    thpool_init(&pool, nTh);
    
    struct Task *task = malloc(sizeof(struct Task));
    task->f = thqsort_real_sort;

    struct TaskArg *arg = malloc(sizeof(struct TaskArg));
    arg->a = a;
    arg->sz = sz;
    arg->depth = depth;
    arg->pool = &pool;

    task->arg = (void *)arg;
    
    thpool_submit(&pool, task);
    wait_for_all_tasks(task);
    
    thpool_finit(&pool);
}