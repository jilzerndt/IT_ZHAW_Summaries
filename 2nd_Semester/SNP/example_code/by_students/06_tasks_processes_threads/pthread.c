#include <sys/types.h>
#include <pthread.h>
#include <stdio.h>

void* worker(void* arg) {
    static int returnValue = 1234;
    printf("Hello :) I'm a worker!");
    return &returnValue;
}

int main(void) {
    // Create a new thread
    pthread_t thread;

    /**
     * Use 'pthread_create' to create a new thread.
     * The first and third parameter are required! The second and fourth may be NULL.
     * The first parameter is a pointer to the 'pthread' to initialize.
     * The third parameter is a pointer to the function to start inside the thread.
     * The second and fourth argument are optional.
     * The fourth parameter allows parameters to be passed to the function.
     */
    if (pthread_create(&thread, NULL, worker, NULL) != 0) {
        // A return value greater zero indicates an error.
        return 1;
    }

    static void *retVal;

    /**
     * Use 'pthread_join' to wait for the passed thread to terminate.
     * To ignore the return value, pass NULL as the second parameter.
     */
    pthread_join(thread, &retVal);
    printf("Worker exited with %d\n", *((int*)retVal));

    /**
     * Use pthread_detach() to to indicate that the kernel may reclaim the thread,
     * as soon as it terminates and does not have to wait for 'pthread_join()'.
     * After calling 'pthread_detach()', 'pthread_join()' must not be called on the
     * same thread.
     */
    //pthread_detach(thread);

    /**
     * Use 'pthread_cancel' to cancel a thread.
     */
    //pthread_cancel(thread);
    return 0;
}