#ifndef __THREAD_QSORT_H__
#define __THREAD_QSORT_H__

#include <stdlib.h>
#include <stdio.h>
#include "thread_pool.h"

struct TaskArg {
    int *a;
    int sz;
    int depth;
    struct ThreadPool *pool;
    struct Task *left, *right;
};

void thqsort(int *a, int sz, int nTh, int depth);

#endif