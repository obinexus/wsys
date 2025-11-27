/* plp128.c */
#include "plp128.h"
#include <math.h>
#include <string.h>

static uint8_t bloom[128];   /* 128-byte filter – unused in minimal demo */

void plp_load(const uint8_t *buf)
{
    memcpy(bloom, buf, 128);
}

/* r = hypot(x,y) ; θ = atan2(y,x) * 180/π */
int plp_cart2pol(double x, double y, double out[2])
{
    out[0] = hypot(x, y);
    out[1] = atan2(y, x) * 180.0 / M_PI;
    return 0;
}

/* x = r * cos(θ); y = r * sin(θ) */
int plp_pol2cart(double r, double theta_deg, double out[2])
{
    double rad = theta_deg * M_PI / 180.0;
    out[0] = r * cos(rad);
    out[1] = r * sin(rad);
    return 0;
}
