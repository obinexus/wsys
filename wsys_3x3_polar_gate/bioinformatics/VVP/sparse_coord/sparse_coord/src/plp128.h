/* plp128.h – PLP-128 minimal API (128-byte Bloom + coord conversion) */
#ifndef PLP128_H
#define PLP128_H

#include <stdint.h>

/* Load a 128-byte Bloom filter (optional – used only for full PLP) */
void plp_load(const uint8_t *bloom128);

/* Cartesian → Polar (r, θ in **degrees**) */
int plp_cart2pol(double x, double y, double out[2]);

/* Polar → Cartesian (x, y) */
int plp_pol2cart(double r, double theta_deg, double out[2]);

#endif /* PLP128_H */
