#include <stdio.h>
#include <stdlib.h>

// Define the dlnode structure
typedef struct dlnode {
    double x[4];                  // The data vector
    struct dlnode *closest[2];    // closest[0] == cx, closest[1] == cy
    struct dlnode *cnext[2];      // current next
    struct dlnode *next[4];       // keeps the points sorted according to coordinates 2, 3, and 4
                                   // (in the case of 2 and 3, only the points swept by 4 are kept)
    struct dlnode *prev[4];       // keeps the points sorted according to coordinates 2 and 3 (except the sentinel 3)
    int ndomr;                    // number of dominators
} dlnode_t;

int main() {
    // Create an instance of the dlnode structure
    dlnode_t *node = (dlnode_t *)malloc(sizeof(dlnode_t));

    // Assign values to its attributes
    node->x[0] = 1.0;
    node->x[1] = 2.0;
    node->x[2] = 3.0;
    node->x[3] = 4.0;

    node->closest[0] = NULL;
    node->closest[1] = NULL;

    node->cnext[0] = NULL;
    node->cnext[1] = NULL;

    node->next[0] = NULL;
    node->next[1] = NULL;
    node->next[2] = NULL;
    node->next[3] = NULL;

    node->prev[0] = NULL;
    node->prev[1] = NULL;
    node->prev[2] = NULL;
    node->prev[3] = NULL;

    node->ndomr = 0;

    // Print the values of the node's attributes
    printf("Node values:\n");
    printf("x[0]: %f\n", node->x[0]);
    printf("x[1]: %f\n", node->x[1]);
    printf("x[2]: %f\n", node->x[2]);
    printf("x[3]: %f\n", node->x[3]);
    printf("closest[0]: %p\n", (void *)node->closest[0]);
    printf("closest[1]: %p\n", (void *)node->closest[1]);
    printf("cnext[0]: %p\n", (void *)node->cnext[0]);
    printf("cnext[1]: %p\n", (void *)node->cnext[1]);
    printf("next[0]: %p\n", (void *)node->next[0]);
    printf("next[1]: %p\n", (void *)node->next[1]);
    printf("next[2]: %p\n", (void *)node->next[2]);
    printf("next[3]: %p\n", (void *)node->next[3]);
    printf("prev[0]: %p\n", (void *)node->prev[0]);
    printf("prev[1]: %p\n", (void *)node->prev[1]);
    printf("prev[2]: %p\n", (void *)node->prev[2]);
    printf("prev[3]: %p\n", (void *)node->prev[3]);
    printf("ndomr: %d\n", node->ndomr);

    // Free the memory allocated for the node
    free(node);

    return 0;
}
