#ifndef PLP128_H
#define PLP128_H
#include <stdint.h>
void plp_load(const uint8_t *bloom128);
int plp_cart2pol(double x, double y, double out[2]);
int plp_pol2cart(double r, double theta_deg, double out[2]);
#endif
