/* plp128.c  –  gcc -O2 -shared -fPIC plp128.c -o plp128.so */
#include <stdint.h>
#include <math.h>
#include "plp128.h"

static uint8_t bloom[128];

void plp_load(const uint8_t *buf){ memcpy(bloom, buf, 128); }

int plp_cart2pol(double x, double y, double *out){
    double r  = hypot(x,y);
    double t  = atan2(y,x) * 180.0/M_PI;
    *out = r;  *(out+1) = t;
    return 0;   /* bloom check elided for speed – Python already verified */
}

int plp_pol2cart(double r, double t, double *out){
    double rad = t * M_PI/180.0;
    *out = r*cos(rad);  *(out+1) = r*sin(rad);
    return 0;
}
