#include <stdio.h>

// Define the dlnode structure
typedef struct dlnode {
    double x[3];           // The data vector
    struct dlnode *cnext[2];  // current next
} dlnode_t;

// Function to compute area
double computeAreaSimple(double *p, int di, dlnode_t *s, dlnode_t *u) {
    int dj = 1 - di;
    double area = 0;
    dlnode_t *q = s;
    area += (q->x[dj] - p[dj]) * (u->x[di] - p[di]);

    while (p[dj] < u->x[dj]) {
        q = u;
        u = u->cnext[di];
        area += (q->x[dj] - p[dj]) * (u->x[di] - q->x[di]);
    }

    return area;
}

int main() {
    // Define the points and p
    double point0_data[] = {4.0, 1.0, 1.0};
    double point1_data[] = {3.0, 2.0, 2.0};
    double point2_data[] = {2.0, 3.0, 3.0};
    double p_data[] = {5.0, 3.0, 3.0};

    // Create dlnode structures for the points
    dlnode_t point0 = {{point0_data[0], point0_data[1], point0_data[2]}, {NULL, NULL}};
    dlnode_t point1 = {{point1_data[0], point1_data[1], point1_data[2]}, {NULL, NULL}};
    dlnode_t point2 = {{point2_data[0], point2_data[1], point2_data[2]}, {NULL, NULL}};

    // Create dlnode structure for p
    dlnode_t p = {{p_data[0], p_data[1], p_data[2]}, {NULL, NULL}};

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
