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
    printf("Result of lexicographicless: %d", c);
}
