#include <stdio.h>
#include <pthread.h>
#include <unistd.h>     // sleep()

void* worker(void* args);

pthread_mutex_t lock;

int main(void) {
    if (pthread_mutex_init(&lock, NULL) != 0) {
        printf("Failed to init mutex\n");
        return 1;
    }

    pthread_t threadA;
    pthread_t threadB;
    pthread_create(&threadA, NULL, worker, "A");
    pthread_create(&threadB, NULL, worker, "B");

    pthread_join(threadA, NULL);
    pthread_join(threadB, NULL);

    return 0;
}

void* worker(void* args) {
    char* name = (char*)args;

    int counter = 10;
    while (counter > 0) {
        printf("Thread %s: Trying to acquire lock\n", name);

        pthread_mutex_lock(&lock); // lock anfordern
        printf("Thread %s: Acquired lock\n", name);

        printf("Thread %s: %d\n", name, counter);
        sleep(2);

        printf("Thread %s: Releasing lock\n", name);
        pthread_mutex_unlock(&lock);    // lock freigeben
        sleep(2);
        counter--;
    }
}