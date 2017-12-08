#include <stdlib.h>
#include <stdio.h>

#include "thread_qsort.h"

int main(int argc, char **argv) {

    int nTh, sz, depth;
    if (argc != 4 || sscanf(argv[1], "%d", &nTh) != 1 || sscanf(argv[2], "%d", &sz) != 1 || sscanf(argv[3], "%d", &depth) != 1) {
        printf("Usage: ./pqsort <number of threads> <array size> <recursion depth>\n");
        return 0;
    }
    
    int *a = malloc(sizeof(int) * sz);
    srand(42);
    for (int i = 0; i < sz; ++i) {
        // a[i] = rand();
        a[i] = rand() % 10;
    }

    thqsort(a, sz, nTh, depth);

    for (int i = 0; i < sz - 1; ++i) {
        if (a[i] > a[i + 1]) {
            printf("Unfortunately, your qsort doesn't work(\n");
            return 0;
        }
    }

    printf("Hooray!!!\n");
    free(a);

    return 0;
}
