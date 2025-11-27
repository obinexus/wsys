// main.c - Example usage
#include "cartesian_polar_functor.h"
#include <stdio.h>

int main() {
    coordinate_functor_t functor;
    plp_init_functor(&functor);
    
    // Example: Convert Cartesian point (3, 4) to Polar
    cartesian_point_t cart;
    cart.x_bits = encode_cartesian_binary(3.0, 4.0);
    cart.y_bits = 0;
    
    polar_point_t polar = functor.to_polar(cart);
    
    double r, theta;
    decode_polar_binary(polar.r_bits, &r, &theta);
    printf("Cartesian (3,4) -> Polar: r=%.2f, θ=%.2f°\n", r, theta);
    
    // Convert back to verify isomorphism
    cartesian_point_t converted_back = functor.to_cartesian(polar);
    double x, y;
    decode_cartesian_binary(converted_back.x_bits, &x, &y);
    printf("Polar -> Cartesian: (%.2f, %.2f)\n", x, y);
    
    // Validate sparse mapping
    int is_valid = is_sparse_mapping_valid(cart, polar);
    printf("Sparse mapping valid: %d\n", is_valid);
    
    return 0;
}
