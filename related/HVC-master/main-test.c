#include <stdio.h>
#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <string.h>
//#include <hv-plus.h>
#include "hv-plus.h"
#include "hvc-private.h"
//#include "hv-plus.c" 

// int lexicographicLess(double * a, double * b){
//     return (a[2] < b[2] || (a[2] == b[2] && (a[1] < b[1] || (a[1] == b[1] && a[0] <= b[0]))));
// }
// Define the dlnode structure
typedef struct dlnodeNew {
    double x[4];                  // The data vector
    struct dlnodeNew *closest[2];    // closest[0] == cx, closest[1] == cy
    struct dlnodeNew *cnext[2];      // current next
    struct dlnodeNew *next[4];       // keeps the points sorted according to coordinates 2, 3, and 4
                                   // (in the case of 2 and 3, only the points swept by 4 are kept)
    struct dlnodeNew *prev[4];       // keeps the points sorted according to coordinates 2 and 3 (except the sentinel 3)
    int ndomr;                    // number of dominators
} dlnodeNew_t;

static dlnodeNew_t * initSentinels(dlnodeNew_t * list, const double * ref, int d){
 
    dlnodeNew_t * s1 = list;
    dlnodeNew_t * s2 = list + 1;
    dlnodeNew_t * s3 = list + 2;
    
    s1->x[0] = -DBL_MAX;
    s1->x[1] = ref[1];
    s1->x[2] = -DBL_MAX;
    s1->x[3] = -DBL_MAX;
    s1->closest[0] = s2;
    s1->closest[1] = s1;  

    s1->next[2] = s2;
    s1->next[3] = s2;
    s1->cnext[1] = NULL;  
    s1->cnext[0] = NULL; 
    
    s1->prev[2] = s3;
    s1->prev[3] = s3;
    s1->ndomr = 0;

    
    s2->x[0] = ref[0];
    s2->x[1] = -DBL_MAX;
    s2->x[2] = -DBL_MAX;
    s2->x[3] = -DBL_MAX;
    s2->closest[0] = s2; 
    s2->closest[1] = s1; 

    s2->next[2] = s3;
    s2->next[3] = s3;
    s2->cnext[1] = NULL;  
    s2->cnext[0] = NULL;  
    
    s2->prev[2] = s1;
    s2->prev[3] = s1;
    s2->ndomr = 0;

    
    
    s3->x[0] = -INT_MAX; 
    s3->x[1] = -INT_MAX; 
    s3->x[2] = ref[2];
    if(d == 4)
        s3->x[3] = ref[3];
    else
        s3->x[3] = - DBL_MAX;
    s3->closest[0] = s2;
    s3->closest[1] = s1;
    
    s3->next[2] = s1;
    s3->next[3] = NULL;
    s3->cnext[1] = NULL;  
    s3->cnext[0] = NULL;  
    
    s3->prev[2] = s2;
    s3->prev[3] = s2;
    s3->ndomr = 0;

    
    return s1;
    
}


int main() {
    printf("Hello world!\n");
    float testArray[5][4] = {{1.0, 1.0, 1.0, 4.0},{2.0, 2.0, 2.0, 4.0},{3.0, 3.0, 3.0, 4.0},{4.0, 4.0, 4.0, 4.0},{5.0, 5.0, 5.0, 4.0}}; 
    float testPoint[4] = {4.6, 4.6, 4.6, 4.0};
    double a[3] = {10.0, 1.0, 1.0};
    double b[3] = {1.0, 1.0, 1.0};    
    //hvc3d(NULL, 1);
    int c = lexicographicLessNew(a, b);
    //const p1 = {3.0, 1.0, 3.0};
    //const p2 = {2.0, 2.0, 4.0};
    //const q1 = {3.0, 1.0, 3.0, 5.0};
    //const q2 = {2.0, 2.0, 4.0, 6.0};
    //compare_point3d(p1, p2);
    //compare_point4d(q1, q2);
    printf("Result of lexicographicless: %d \n", c);

        // Create an instance of the dlnode structure
    dlnodeNew_t *node1 = (dlnodeNew_t *)malloc(sizeof(dlnodeNew_t));
    dlnodeNew_t *node2 = (dlnodeNew_t *)malloc(sizeof(dlnodeNew_t));
    dlnodeNew_t *node3 = (dlnodeNew_t *)malloc(sizeof(dlnodeNew_t));

    // Assign values to its attributes for node1
    node1->x[0] = 1.0;
    node1->x[1] = 2.0;
    node1->x[2] = 3.0;
    node1->x[3] = 4.0;

    node2->x[0] = 5.0;
    node2->x[1] = 6.0;
    node2->x[2] = 7.0;
    node2->x[3] = 8.0;

    node3->x[0] = 9.0;
    node3->x[1] = 10.0;
    node3->x[2] = 11.0;
    node3->x[3] = 12.0;

    node1->closest[0] = node2;
    node1->closest[1] = NULL;

    node1->cnext[0] = node3;
    node1->cnext[1] = NULL;

    node1->next[0] = node2;
    node1->next[1] = NULL;
    node1->next[2] = NULL;
    node1->next[3] = NULL;

    node1->prev[0] = NULL;
    node1->prev[1] = NULL;
    node1->prev[2] = NULL;
    node1->prev[3] = NULL;

    node1->ndomr = 0;

    node2->prev[0] = node1;


    //Print the values of the node's attributes
    printf("Node1 values:\n");
    printf("x[0]: %f\n", node1->x[0]);
    printf("x[1]: %f\n", node1->x[1]);
    printf("x[2]: %f\n", node1->x[2]);
    printf("x[3]: %f\n", node1->x[3]);

    printf("node1.next[0] coordinates: (%f, %f, %f, %f)\n",
        node1->next[0]->x[0], node1->next[0]->x[1],
        node1->next[0]->x[2], node1->next[0]->x[3]);
    
    printf("node2.prev[0] coordinates: (%f, %f, %f, %f)\n",
        node2->prev[0]->x[0], node2->prev[0]->x[1],
        node2->prev[0]->x[2], node2->prev[0]->x[3]);

    printf("Node2 values:\n");
    printf("x[0]: %f\n", node2->x[0]);
    printf("x[1]: %f\n", node2->x[1]);
    printf("x[2]: %f\n", node2->x[2]);
    printf("x[3]: %f\n", node2->x[3]);

    printf("Node3 values:\n");
    printf("x[0]: %f\n", node3->x[0]);
    printf("x[1]: %f\n", node3->x[1]);
    printf("x[2]: %f\n", node3->x[2]);
    printf("x[3]: %f\n", node3->x[3]);
    //printf("closest[0]: %p\n", (void *)node1->closest[0]);
    //printf("closest[1]: %p\n", (void *)node1->closest[1]);
    //printf("cnext[0]: %p\n", (void *)node1->cnext[0]);
    //printf("cnext[1]: %p\n", (void *)node1->cnext[1]);
    //printf("next[0]: %p\n", (void *)node1->next[0]);
    //printf("next[1]: %p\n", (void *)node1->next[1]);
    //printf("next[2]: %p\n", (void *)node1->next[2]);
    //printf("next[3]: %p\n", (void *)node1->next[3]);
    //printf("prev[0]: %p\n", (void *)node1->prev[0]);
    //printf("prev[1]: %p\n", (void *)node1->prev[1]);
    //printf("prev[2]: %p\n", (void *)node1->prev[2]);
    //printf("prev[3]: %p\n", (void *)node1->prev[3]);
    //printf("ndomr: %d\n", node1->ndomr);

    // Free the memory allocated for the node
    free(node1);

    // Define reference point and list
    double ref[] = {1.0, 2.0, 3.0, 4.0};
    dlnodeNew_t list[3];

    // Initialize sentinel nodes
    dlnodeNew_t *head = initSentinels(list, ref, 4);

    // Print values of the sentinel nodes
    printf("Sentinel node s1 values:\n");
    printf("x[0]: %f\n", head->x[0]);
    printf("x[1]: %f\n", head->x[1]);
    printf("x[2]: %f\n", head->x[2]);
    printf("x[3]: %f\n", head->x[3]);
    printf("closest[0]: %p\n", (void *)head->closest[0]);
    //printf("closest[1]: %p\n", (void *)head->closest[1]);
    //printf("next[2]: %p\n", (void *)head->next[2]);
    //printf("next[3]: %p\n", (void *)head->next[3]);
    //printf("prev[2]: %p\n", (void *)head->prev[2]);
    //printf("prev[3]: %p\n", (void *)head->prev[3]);
    //printf("ndomr: %d\n", head->ndomr);

    printf("closest[0] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->closest[0]->x[0], head->closest[0]->x[1],
        head->closest[0]->x[2], head->closest[0]->x[3]);
    printf("closest[1] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->closest[1]->x[0], head->closest[1]->x[1],
        head->closest[1]->x[2], head->closest[1]->x[3]);
    printf("next[2] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->next[2]->x[0], head->next[2]->x[1],
        head->next[2]->x[2], head->next[2]->x[3]);
    printf("next[3] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->next[3]->x[0], head->next[3]->x[1],
        head->next[3]->x[2], head->next[3]->x[3]);
    printf("prev[2] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->prev[2]->x[0], head->prev[2]->x[1],
        head->prev[2]->x[2], head->prev[2]->x[3]);
    printf("prev[3] coordinates: (%f \n, %f \n, %f \n, %f \n)\n",
        head->prev[3]->x[0], head->prev[3]->x[1],
        head->prev[3]->x[2], head->prev[3]->x[3]);
    printf("ndomr: %d\n", head->ndomr);

    return 0;
}
