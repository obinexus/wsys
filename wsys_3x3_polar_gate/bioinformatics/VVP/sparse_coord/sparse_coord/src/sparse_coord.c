/* sparse_coord.c  –  O(1) auxiliary space, real-time PLP functor */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

#define HINT_BYTES 1                     // 2 bits are enough
#define CARTESIAN_HINT  0b10             // binary 10
#define POLAR_HINT      0b01             // binary 01

typedef struct { double x, y; } Cart;
typedef struct { double r, theta; } Pol;

static uint8_t read_hint(const char *path)
{
    FILE *f = fopen(path, "rb");
    if (!f) { perror(path); exit(1); }
    uint8_t b = 0;
    fread(&b, 1, 1, f);
    fclose(f);
    return b & 0x03;                     // keep lower 2 bits
}

/* ----------  FUNCTOR  ---------- */
void sparse_coord_functor(Cart *c, Pol *p, int have_c, int have_p)
{
    uint8_t hint_c = read_hint("cartesian.bin");
    uint8_t hint_p = read_hint("polar.bin");

    if (have_c && have_p) {                     // both – verify
        double rx = p->r * cos(p->theta);
        double ry = p->r * sin(p->theta);
        if (fabs(rx - c->x) > 1e-9 || fabs(ry - c->y) > 1e-9)
            fprintf(stderr, "Warning: isomorphism broken!\n");
        return;
    }

    if (have_c) {                               // Cartesian → Polar
        if (hint_p != POLAR_HINT) {
            fprintf(stderr, "polar hint mismatch\n"); exit(1);
        }
        p->r     = sqrt(c->x*c->x + c->y*c->y);
        p->theta = atan2(c->y, c->x);
    } else {                                    // Polar → Cartesian
        if (hint_c != CARTESIAN_HINT) {
            fprintf(stderr, "cartesian hint mismatch\n"); exit(1);
        }
        c->x = p->r * cos(p->theta);
        c->y = p->r * sin(p->theta);
    }
}

/* ----------  Demo driver  ---------- */
int main(void)
{
    Cart c = { .x = 12.0, .y = 5.0 };
    Pol  p = {0};

    sparse_coord_functor(&c, &p, 1, 0);         // only Cartesian given
    printf("Polar: r = %.3f  θ = %.3f°\n", p.r, p.theta * 180 / M_PI);

    // now pretend we only have Polar
    Pol  p2 = { .r = 13.0, .theta = 22.6 * M_PI / 180 };
    Cart c2 = {0};
    sparse_coord_functor(&c2, &p2, 0, 1);
    printf("Cartesian: x = %.3f  y = %.3f\n", c2.x, c2.y);
    return 0;
}
