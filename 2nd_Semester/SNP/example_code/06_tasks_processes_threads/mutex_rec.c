#include <sys/types.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

void nestedLock();

pthread_mutexattr_t mutex_attr;
pthread_mutex_t mutex;

int main(void) {
    if (pthread_mutexattr_init(&mutex_attr) != 0) {
        printf("Failed to init mutex attr\n");
        return 1;
    }

    if (pthread_mutexattr_settype(&mutex_attr, PTHREAD_MUTEX_RECURSIVE) != 0) {
        printf("Failed to  mutex attribute type\n");
        return 2;
    }

    if (pthread_mutex_init(&mutex, &mutex_attr) != 0) {
        printf("Failed to init mutex\n");
        return 3;
    }

    printf("Lock in 'main'\n");
    pthread_mutex_lock(&mutex); // mutex anfordern

    nestedLock();

    printf("Unlock in 'main'\n");
    pthread_mutex_unlock(&mutex);    // mutex freigeben

    return 0;
}

void nestedLock() {
    // Würde ohne mutex attribute failen
    printf("- Lock in 'nestedLock'\n");
    if (pthread_mutex_lock(&mutex) != 0) {
        perror("Failed to acquire lock\n");
        exit(EXIT_FAILURE);
    }

    printf("- - Successfully claimed lock.\n");

    printf("- Unlock in 'nestedLock'\n");
    if (pthread_mutex_unlock(&mutex) != 0) {
        perror("Failed to free lock\n");
        exit(EXIT_FAILURE);
    }
}
