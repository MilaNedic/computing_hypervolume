#include <stdio.h>
#include <stdlib.h>
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


static int compare_point3d(const void *p1, const void* p2)
{
    int i;
    for(i = 2; i >= 0; i--){
        double x1 = (*((const double **)p1))[i];
        double x2 = (*((const double **)p2))[i];

        if(x1 < x2)
            return -1;
        if(x1 > x2)
            return 1;
    }
    return 0;
}


static int compare_point4d(const void *p1, const void* p2)
{
    int i;
    for(i = 3; i >= 0; i--){
        double x1 = (*((const double **)p1))[i];
        double x2 = (*((const double **)p2))[i];

        if(x1 < x2)
            return -1;
        if(x1 > x2)
            return 1;
    }
    return 0;
}

static void addToZ(dlnode_t * new){
    
    new->next[2] = new->prev[2]->next[2]; //in case new->next[2] was removed for being dominated
    
    new->next[2]->prev[2] = new;
    new->prev[2]->next[2] = new;
}


static void removeFromZ(dlnode_t * old){
    old->prev[2]->next[2] = old->next[2];
    old->next[2]->prev[2] = old->prev[2];
}


static void setupZandClosest(dlnodeNew_t *list, dlnodeNew_t *new) {
    double *closest1 = (double *)(list);
    double *closest0 = (double *)(list->next[2]);

    dlnodeNew_t *q = (list->next[2]->next[2]);
    double *newx = new->x;

    while(q != NULL && lexicographicLessNew(q->x, newx)){
        if(q->x[0] <= newx[0] && q->x[1] <= newx[1]){
            new->ndomr += 1;
        }else if(q->x[1] < newx[1] && (q->x[0] < closest0[0] || (q->x[0] == closest0[0] && q->x[1] < closest0[1]))){
            closest0 = (double *) q;
        }else if(q->x[0] < newx[0] && (q->x[1] < closest1[1] || (q->x[1] == closest1[1] && q->x[0] < closest1[0]))){
            closest1 = (double *) q;
        }

        q = q->next[2];
    }

    new->closest[0] = new->cnext[0] = (dlnodeNew_t *) closest0;
    new->closest[1] = new->cnext[1] = (dlnodeNew_t *) closest1;
    
    if (q != NULL) {
        new->prev[2] = q->prev[2];
        new->next[2] = q;
        if (q->prev[2]) {
            q->prev[2]->next[2] = new;
        }
        q->prev[2] = new;
    }
}

int main() {
    printf("Hello world!\n");


}
