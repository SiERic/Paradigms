CC = gcc
CFLAGS = -Wall -Werror -Wextra -Wshadow -I ./include
# INCLUDES = include/clist.h include/position.h


all: pqsort

bin:
	mkdir -p bin

pqsort: bin/pqsort.o bin/linkedlist.o bin/queue.o bin/squeue.o bin/wsqueue.o bin/thread_pool.o bin/thread_qsort.o include/*.h bin
	$(CC) bin/*.o -o pqsort -lpthread 

bin/linkedlist.o: src/linkedlist.c include/*.h bin
	$(CC) $(CFLAGS) -c src/linkedlist.c -o bin/linkedlist.o

bin/queue.o: src/queue.c include/*.h bin
	$(CC) $(CFLAGS) -c src/queue.c -o bin/queue.o

bin/squeue.o: src/squeue.c include/*.h bin
	$(CC) $(CFLAGS) -c src/squeue.c -o bin/squeue.o

bin/wsqueue.o: src/wsqueue.c include/*.h bin
	$(CC) $(CFLAGS) -c src/wsqueue.c -o bin/wsqueue.o

bin/thread_pool.o: src/thread_pool.c include/*.h bin
	$(CC) $(CFLAGS) -c src/thread_pool.c -o bin/thread_pool.o

bin/thread_qsort.o: src/thread_qsort.c include/*.h bin
	$(CC) $(CFLAGS) -c src/thread_qsort.c -o bin/thread_qsort.o

bin/pqsort.o: src/pqsort.c include/*.h bin
	$(CC) $(CFLAGS) -c src/pqsort.c -o bin/pqsort.o

clean:
	rm -rf bin pqsort

.PHONY: all clean
