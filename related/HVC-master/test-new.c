#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include "avl.h"

typedef struct dlnodeNew {
    double x[4];                   // The data vector
    struct dlnodeNew *closest[2];  // closest[0] == cx, closest[1] == cy
    struct dlnodeNew *cnext[2];    // current next pointers for rebuild
    struct dlnodeNew *next[4];     // keeps the points sorted according to coordinates
    struct dlnodeNew *prev[4];     // keeps the points sorted according to coordinates
    int ndomr;                     // number of dominators
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

static dlnodeNew_t * point2Struct(dlnodeNew_t * list, dlnodeNew_t * p, double * v, int d){
    
    int i;
    for(i = 0; i < d; i++)
        p->x[i] = v[i];
    
    
    clearPoint(list, p);
    
    return p;
    
}


static void addToZ(dlnodeNew_t * new){
    
    new->next[2] = new->prev[2]->next[2]; //in case new->next[2] was removed for being dominated
    
    new->next[2]->prev[2] = new;
    new->prev[2]->next[2] = new;
}


static void removeFromz(dlnodeNew_t * old){
    old->prev[2]->next[2] = old->next[2];
    old->next[2]->prev[2] = old->prev[2];
}


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

static double computeAreaSimple(double * p, int di, dlnodeNew_t * s, dlnodeNew_t * u){

    int dj = 1 - di;
    double area = 0;
    dlnodeNew_t * q = s;
    area += (q->x[dj] - p[dj]) * (u->x[di] - p[di]);
    
    while(p[dj] < u->x[dj]){

        q = u;
        u = u->cnext[di];
        area += (q->x[dj] - p[dj]) * (u->x[di] - q->x[di]);

    }
 
    return area;
}

static double oneContribution3d(dlnodeNew_t * list, dlnodeNew_t * new){
    
//     int considerDominated = 1;
    
    dlnodeNew_t * p = list;
    double area = 0;
    double volume = 0;
    double x[3];
    
    restartBaseSetupZandClosest(list, new);
    if (new->ndomr > 0)
        return 0;
    
    new->cnext[0] = new->closest[0];
    new->cnext[1] = new->closest[1];
    area = computeAreaSimple(new->x, 1, new->cnext[0], new->cnext[0]->cnext[1]);
    
    p = new->next[2];
    double lastz = new->x[2];
    
    while(p->x[0] > new->x[0] || p->x[1] > new->x[1]){
        volume += area * (p->x[2]- lastz);
            p->cnext[0] = p->closest[0];
            p->cnext[1] = p->closest[1];
            
            
            if(p->x[0] >= new->x[0] && p->x[1] >= new->x[1]){
                area -= computeAreaSimple(p->x, 1, p->cnext[0], p->cnext[0]->cnext[1]);
                p->cnext[1]->cnext[0] = p;
                p->cnext[0]->cnext[1] = p;
                
            }else if(p->x[0] >= new->x[0]){
                if(p->x[0] <= new->cnext[0]->x[0]){
                    x[0] = p->x[0]; x[1] = new->x[1]; x[2] = p->x[2]; 
                    area -= computeAreaSimple(x, 1, new->cnext[0], new->cnext[0]->cnext[1]);
                    p->cnext[0] = new->cnext[0];
                    p->cnext[1]->cnext[0] = p;
                    new->cnext[0] = p;
                }
            }else{
                if(p->x[1] <= new->cnext[1]->x[1]){
                    x[0] = new->x[0]; x[1] = p->x[1]; x[2] = p->x[2]; 
                    area -= computeAreaSimple(x, 0, new->cnext[1], new->cnext[1]->cnext[0]);
                    p->cnext[1] = new->cnext[1];
                    p->cnext[0]->cnext[1] = p;
                    new->cnext[1] = p;
                }
                
            }
        lastz = p->x[2];
        p = p->next[2];
        
    }
    
    volume += area * (p->x[2]- lastz);
    return volume;
    
}

int compare_point3d(const void *p1, const void* p2)
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



int compare_point4d(const void *p1, const void* p2)
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

static dlnodeNew_t *
setup_cdllist(double * data, int naloc, int n, int d, const double *ref)
{
    int di = d-1;
    
    dlnodeNew_t * head = (dlnodeNew_t *) malloc((naloc+3) * sizeof(dlnodeNew_t));
    int i;
    dlnodeNew_t * list = head;
    initSentinels(head, ref, d);
    
    if(n > 0){
        double **scratchd;
        int j;
        scratchd = malloc(n * sizeof(double*));
        double * data2 = (double *) malloc(d * n * sizeof(double));
        
        for (i = 0; i < n; i++) {
            scratchd[i] = &data[d*i];   
        }
        
        if(d == 3)
            qsort(scratchd, n, sizeof(double*), compare_point3d);
        else if(d == 4)
            qsort(scratchd, n, sizeof(double*), compare_point4d);
        
        for(i = 0; i < n; i++){
    //             printf("%f\n", scratchd[i][2]);
            for(j = 0; j < d; j++){
                data2[d * i + j] = scratchd[i][j];
            }
        }
        
        
    //     int d = 3;
        dlnodeNew_t ** scratch = (dlnodeNew_t **) malloc(n * sizeof(dlnodeNew_t *));

        for (i = 0; i < n; i++) {
            scratch[i] = point2Struct(list, head+i+3, &data2[i*d], d);
    //             scratch[i] = newPoint(head, &data[i*d], d);   
//             scratch[i]->id = order[i];
//             scratch[i]->id = (scratchd[i]-data)/3;
        }

        
        free(scratchd);
        
        
        dlnodeNew_t * s = head->next[di];
        s->next[di] = scratch[0];
        scratch[0]->prev[di] = s;

                
        for(i = 0; i < n-1; i++){
            scratch[i]->next[di] = scratch[i+1];
            scratch[i+1]->prev[di] = scratch[i];
        }
        
        s = head->prev[di];
        s->prev[di] = scratch[n-1];
        scratch[n-1]->next[di] = s;
        
        free(scratch);
        free(data2);
    }
    
    return head;
}

static double hv3dplus(dlnodeNew_t * list){
    
    dlnodeNew_t * p = list;
    double area = 0;
    double volume = 0;
    
    restartListy(list);
    p = p->next[2]->next[2];
    
    dlnodeNew_t * stop = list->prev[2];
    
    while(p != stop){
        if(p->ndomr < 1){
            p->cnext[0] = p->closest[0];
            p->cnext[1] = p->closest[1];

            printf("current p [%lf, %lf, %lf, %lf]\n", p->x[0], p->x[1], p->x[2], p->x[3]);
            printf("p->closest[0] [%lf, %lf, %lf, %lf]\n", p->closest[0]->x[0], p->closest[0]->x[1], p->closest[0]->x[2], p->closest[0]->x[3]);
            printf("p->closest[1] [%lf, %lf, %lf, %lf]\n", p->closest[1]->x[0], p->closest[1]->x[1], p->closest[1]->x[2], p->closest[1]->x[3]);
            printf("p->cnext[0] [%lf, %lf, %lf, %lf]\n", p->cnext[0]->x[0], p->cnext[0]->x[1], p->cnext[0]->x[2], p->cnext[0]->x[3]);
            printf("p->cnext[0]->cnext[1] [%lf, %lf, %lf, %lf]\n", p->cnext[0]->cnext[1]->x[0], p->cnext[0]->cnext[1]->x[1], p->cnext[0]->cnext[1]->x[2], p->cnext[0]->cnext[1]->x[3]);

            area += computeAreaSimple(p->x, 1, p->cnext[0], p->cnext[0]->cnext[1]);
            
            p->cnext[0]->cnext[1] = p;
            p->cnext[1]->cnext[0] = p;
        }else{
            removeFromz(p);
        }
        
        volume += area * (p->next[2]->x[2]- p->x[2]);
        
        p = p->next[2];
    }
    
    //printf("hv3dplusU");

    return volume;
    
}

static void free_cdllist(dlnodeNew_t * list)
{
    free(list);
}

static int compare_tree_asc_y( const void *p1, const void *p2)
{
    const double x1= *((const double *)p1+1);
    const double x2= *((const double *)p2+1);

    if (x1 < x2)
        return -1;
    else if (x1 > x2)
        return 1;
    else return 0;
}


static inline double *node_point(const avl_node_t *node)
{
    return (double*) node->item;
}



int main() {
    printf("Test\n");
    // Provided data
    // Provided data
    double points[] = {
        0.16, 0.86, 0.47,
        0.66, 0.37, 0.29,
        0.79, 0.79, 0.04,
        0.28, 0.99, 0.29,
        0.51, 0.37, 0.38,
        0.92, 0.62, 0.07,
        0.16, 0.53, 0.70,
        0.01, 0.98, 0.94,
        0.67, 0.17, 0.54,
        0.79, 0.72, 0.05
    };
    double ref_p[] = {1.0, 1.0, 1.0};
    int naloc = 10; // You need to specify the value of naloc
    int n = 10;     // Number of points
    int d = 3;     // Dimensionality

    // Setup the cdllist
    dlnodeNew_t *head = setup_cdllist(points, naloc, n, d, ref_p);

    // Print out the nodes in the cdllist
    printf("Nodes in the cdllist:\n");
    dlnodeNew_t *current = head->next[d - 1]; // Start from the first node
    int count = 0;
    while (current != head) {
        printf("[%lf, %lf, %lf, %lf]\n", current->x[0], current->x[1], current->x[2], current->x[3]);
        current = current->next[d - 1];
        count++;
    }

    // Compute the hypervolume in 3D
    double hypervolume = hv3dplus(head);

    // Print out the hypervolume
    printf("Hypervolume in 3D: %lf\n", hypervolume);

    // Free dynamically allocated memory
    // You should free all dynamically allocated memory here
    // Freeing the cdllist is not included in this example
    free_cdllist(head);
    return 0;
}