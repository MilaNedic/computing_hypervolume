#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <float.h>
#include <string.h>

typedef struct dlnodeNew {
    double x[4];                   // The data vector
    struct dlnodeNew *closest[2];  // closest[0] == cx, closest[1] == cy
    struct dlnodeNew *cnext[2];    // current next pointers for rebuild
    struct dlnodeNew *next[4];     // keeps the points sorted according to coordinates
    struct dlnodeNew *prev[4];     // keeps the points sorted according to coordinates
    int ndomr;                     // number of dominators
} dlnodeNew_t;

static void restartListy(dlnodeNew_t *list) {
    list->next[2]->cnext[1] = list;  // Link sentinels
    list->cnext[0] = list->next[2];  // Assume list->next[2] is a sentinel with smallest values
}

static int lexicographicLess(double *a, double *b) {
    return (a[2] < b[2] || (a[2] == b[2] && (a[1] < b[1] || (a[1] == b[1] && a[0] <= b[0]))));
}

static void restartBaseSetupZandClosest(dlnodeNew_t *list, dlnodeNew_t *new) {
    dlnodeNew_t *p = list->next[2]->next[2];
    double *closest1 = (double *)(list);
    double *closest0 = (double *)(list->next[2]);

    double *newx = new->x;
    
    restartListy(list);
    
    while (p && lexicographicLess(p->x, newx)) {
        p->cnext[0] = p->closest[0];
        p->cnext[1] = p->closest[1];
        
        p->cnext[0]->cnext[1] = p;
        p->cnext[1]->cnext[0] = p;
        
        if (p->x[0] <= newx[0] && p->x[1] <= newx[1]) {
            new->ndomr += 1;
        } else if (p->x[1] < newx[1] && (p->x[0] < closest0[0] || (p->x[0] == closest0[0] && p->x[1] < closest0[1]))) {
            closest0 = (double *) p;
        } else if (p->x[0] < newx[0] && (p->x[1] < closest1[1] || (p->x[1] == closest1[1] && p->x[0] < closest1[0]))) {
            closest1 = (double *) p;
        }
        p = p->next[2];
    }
    
    new->closest[0] = (dlnodeNew_t *) closest0;
    new->closest[1] = (dlnodeNew_t *) closest1;
    new->prev[2] = p ? p->prev[2] : NULL;
    new->next[2] = p;
}

int main() {
    dlnodeNew_t *list = malloc(sizeof(dlnodeNew_t));
    dlnodeNew_t *newNode = malloc(sizeof(dlnodeNew_t));
    dlnodeNew_t *node1 = malloc(sizeof(dlnodeNew_t));
    dlnodeNew_t *node2 = malloc(sizeof(dlnodeNew_t));

    // Initialize nodes
    list->x[0] = -1; list->x[1] = -1; list->x[2] = -1; list->x[3] = -1;
    node1->x[0] = 0; node1->x[1] = 0; node1->x[2] = 0; node1->x[3] = 0;
    node2->x[0] = 5; node2->x[1] = 5; node2->x[2] = 5; node2->x[3] = 5;
    newNode->x[0] = 1; newNode->x[1] = 1; newNode->x[2] = 2; newNode->x[3] = 2;

    // Link nodes
    list->next[2] = node1;
    node1->next[2] = node2;
    node2->next[2] = NULL;

    // Setup the list and new node interaction
    restartBaseSetupZandClosest(list, newNode);

    printf("New node dominators count: %d\n", newNode->ndomr);
    printf("New node closest[0]: (%.1f, %.1f, %.1f, %.1f)\n", newNode->closest[0]->x[0], newNode->closest[0]->x[1], newNode->closest[0]->x[2], newNode->closest[0]->x[3]);
    printf("New node closest[1]: (%.1f, %.1f, %.1f, %.1f)\n", newNode->closest[1]->x[0], newNode->closest[1]->x[1], newNode->closest[1]->x[2], newNode->closest[1]->x[3]);

    free(list);
    free(newNode);
    free(node1);
    free(node2);

    return 0;
}