/* Code for different types of semaphores in C
    Base case: Mutex
    1. Binary Semaphore
    2. Counting Semaphore
    3. Fair Semaphore (FIFO Semaphore)
    4. Named Semaphore
    5. Unnamed Semaphore
    6. Producer-Consumer Problem (Bounded Buffer)
*/

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>     // sleep()

/*
----------------------------------------
Binary Semaphore

A binary semaphore is a semaphore which can have only two values - 0 and 1. 
Its primary use is as a synchronization tool between threads, to solve the critical section problem for instance.
----------------------------------------
*/
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t binary_semaphore;

void* function1(void* arg) {
    sem_wait(&binary_semaphore); // Decrease the semaphore value
    printf("Hello from function1\n");
    sem_post(&binary_semaphore); // Increase the semaphore value
    return NULL;
}

void* function2(void* arg) {
    sem_wait(&binary_semaphore); // Decrease the semaphore value
    printf("Hello from function2\n");
    sem_post(&binary_semaphore); // Increase the semaphore value
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    // Initialize binary semaphore
    sem_init(&binary_semaphore, 0, 1);

    pthread_create(&thread1, NULL, function1, NULL);
    pthread_create(&thread2, NULL, function2, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    // Destroy binary semaphore
    sem_destroy(&binary_semaphore);

    return 0;
}

/*
----------------------------------------
Counting Semaphore

A counting semaphore is a semaphore that can have arbitrary values, not just 0 and 1. 
It can be used to control access to a resource with multiple instances, or to synchronize multiple threads
----------------------------------------
*/
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define NUM_THREADS 10

sem_t counting_semaphore;

void* function(void* arg) {
    sem_wait(&counting_semaphore); // Decrease the semaphore value
    printf("Thread %ld is using the resource\n", (long)arg);
    sem_post(&counting_semaphore); // Increase the semaphore value
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];

    // Initialize counting semaphore with a value of 5
    sem_init(&counting_semaphore, 0, 5);

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, function, (void*)i);
    }

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    // Destroy counting semaphore
    sem_destroy(&counting_semaphore);

    return 0;
}

/*
----------------------------------------
Fair Semaphore

A fair semaphore, also known as a FIFO semaphore, ensures that threads acquire the semaphore in the order they request it, preventing starvation.
POSIX semaphores are not fair by default, but you can implement a fair semaphore using a mutex and a condition variable.
----------------------------------------
*/
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define NUM_THREADS 10

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int count;
} fair_semaphore_t;

fair_semaphore_t fair_semaphore;

void fair_semaphore_init(fair_semaphore_t* sem, int value) {
    pthread_mutex_init(&sem->mutex, NULL);
    pthread_cond_init(&sem->cond, NULL);
    sem->count = value;
}

void fair_semaphore_wait(fair_semaphore_t* sem) {
    pthread_mutex_lock(&sem->mutex);
    while (sem->count <= 0) {
        pthread_cond_wait(&sem->cond, &sem->mutex);
    }
    sem->count--;
    pthread_mutex_unlock(&sem->mutex);
}

void fair_semaphore_post(fair_semaphore_t* sem) {
    pthread_mutex_lock(&sem->mutex);
    sem->count++;
    pthread_cond_signal(&sem->cond);
    pthread_mutex_unlock(&sem->mutex);
}

void* function(void* arg) {
    fair_semaphore_wait(&fair_semaphore);
    printf("Thread %ld is using the resource\n", (long)arg);
    fair_semaphore_post(&fair_semaphore);
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];

    // Initialize fair semaphore with a value of 5
    fair_semaphore_init(&fair_semaphore, 5);

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, function, (void*)i);
    }

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}

/*
----------------------------------------
Named Semaphore

A named semaphore is a type of semaphore that can be accessed by different processes, not just threads of the same process. 
Named semaphores are identified by a name in the file system.
----------------------------------------
*/
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <semaphore.h>
#include <unistd.h>

#define SEM_NAME "/my_named_semaphore"

int main() {
    sem_t *named_semaphore;

    // Create a named semaphore
    named_semaphore = sem_open(SEM_NAME, O_CREAT, S_IRUSR | S_IWUSR, 1);

    if (fork() == 0) {
        // Child process
        sem_wait(named_semaphore); // Decrease the semaphore value
        printf("Hello from child process\n");
        sem_post(named_semaphore); // Increase the semaphore value
    } else {
        // Parent process
        sem_wait(named_semaphore); // Decrease the semaphore value
        printf("Hello from parent process\n");
        sem_post(named_semaphore); // Increase the semaphore value

        // Wait for child process to finish
        wait(NULL);

        // Close and unlink the named semaphore
        sem_close(named_semaphore);
        sem_unlink(SEM_NAME);
    }

    return 0;
}

/*
----------------------------------------
Unnamed Semaphore

An unnamed semaphore, also known as an anonymous semaphore, is a type of semaphore that can only be accessed by threads of the same process. 
Unnamed semaphores are typically stored in shared memory.
----------------------------------------
*/

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t unnamed_semaphore;

void* function1(void* arg) {
    sem_wait(&unnamed_semaphore); // Decrease the semaphore value
    printf("Hello from function1\n");
    sem_post(&unnamed_semaphore); // Increase the semaphore value
    return NULL;
}

void* function2(void* arg) {
    sem_wait(&unnamed_semaphore); // Decrease the semaphore value
    printf("Hello from function2\n");
    sem_post(&unnamed_semaphore); // Increase the semaphore value
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    // Initialize unnamed semaphore
    sem_init(&unnamed_semaphore, 0, 1);

    pthread_create(&thread1, NULL, function1, NULL);
    pthread_create(&thread2, NULL, function2, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    // Destroy unnamed semaphore
    sem_destroy(&unnamed_semaphore);

    return 0;
}

/*
----------------------------------------
Producer-Consumer Problem (Bounded Buffer)

The problem describes two processes, the producer and the consumer, who share a common, fixed-size buffer. 
The producer's job is to generate data, put it into the buffer, and start again. 
At the same time, the consumer is consuming the data (i.e., removing it from the buffer), one piece at a time.
----------------------------------------
*/
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define BUFFER_SIZE 10

int buffer[BUFFER_SIZE];
int in = 0;
int out = 0;

sem_t empty;
sem_t full;
pthread_mutex_t mutex;

void* producer(void* arg) {
    for (int i = 0; i < 20; i++) {
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);

        buffer[in] = i;
        printf("Producer produced %d\n", i);
        in = (in + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&full);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 0; i < 20; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);

        int item = buffer[out];
        printf("Consumer consumed %d\n", item);
        out = (out + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&empty);
    }
    return NULL;
}

int main() {
    pthread_t producer_thread, consumer_thread;

    pthread_mutex_init(&mutex, NULL);
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);

    pthread_create(&producer_thread, NULL, producer, NULL);
    pthread_create(&consumer_thread, NULL, consumer, NULL);

    pthread_join(producer_thread, NULL);
    pthread_join(consumer_thread, NULL);

    pthread_mutex_destroy(&mutex);
    sem_destroy(&empty);
    sem_destroy(&full);

    return 0;
}