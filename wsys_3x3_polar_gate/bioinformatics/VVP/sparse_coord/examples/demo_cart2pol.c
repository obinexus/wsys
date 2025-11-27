#include "plp128.h"
#include <stdio.h>

int main(void) {
    double out[2];
    plp_cart2pol(12.0, 5.0, out);
    printf("r = %.6f  θ = %.6f°\n", out[0], out[1]);
    return 0;
}
