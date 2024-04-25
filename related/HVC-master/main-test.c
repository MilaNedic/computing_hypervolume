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

static void clearPoint(dlnodeNew_t * list, dlnodeNew_t * p){
    
    p->closest[1] = list;
    p->closest[0] = list->next[2]; 
    
    /* because of printfs */
    p->cnext[1] = list;
    p->cnext[0] = list->next[2];
    
    
    p->ndomr = 0;
    
}

double computeAreaSimple(double *p, int di, dlnodeNew_t *s, dlnodeNew_t *u) {
    int dj = 1 - di;
    double area = 0;
    dlnodeNew_t *q = s;
    area += (q->x[dj] - p[dj]) * (u->x[di] - p[di]);

    while (p[dj] < u->x[dj]) {
        q = u;
        u = u->cnext[di];
        area += (q->x[dj] - p[dj]) * (u->x[di] - q->x[di]);
    }

    return area;
}


int main() {
    printf("Hello world!\n");
        // Define the points and p
    double point0_data[] = {3.0, 2.0, 2.0, 0.0};
    double point1_data[] = {2.0, 3.0, 3.0, 0.0};
    double p_data[] = {5.0, 3.0, 3.0, 0.0};

    // Create dlnodeNew structures for the points
    dlnodeNew_t point0 = {{point0_data[0], point0_data[1], point0_data[2], point0_data[3]}, {NULL, NULL}, {NULL, NULL}, {NULL, NULL, NULL, NULL}, {NULL, NULL, NULL, NULL}, 0};
    dlnodeNew_t point1 = {{point1_data[0], point1_data[1], point1_data[2], point1_data[3]}, {NULL, NULL}, {NULL, NULL}, {NULL, NULL, NULL, NULL}, {NULL, NULL, NULL, NULL}, 0};

    // Create dlnodeNew structure for p
    dlnodeNew_t p = {{p_data[0], p_data[1], p_data[2], p_data[3]}, {NULL, NULL}, {NULL, NULL}, {NULL, NULL, NULL, NULL}, {NULL, NULL, NULL, NULL}, 5};

    // Compute area for di = 0
    int di = 0;
    double area_di_0 = computeAreaSimple(p_data, di, &point0, &point1);
    printf("Area for di = 0: %f\n", area_di_0);

    // Compute area for di = 1
    di = 1;
    double area_di_1 = computeAreaSimple(p_data, di, &point0, &point1);
    printf("Area for di = 1: %f\n", area_di_1);

    return 0;


}
