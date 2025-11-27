// cartesian_polar_functor.c
#include "cartesian_polar_functor.h"
#include <stdio.h>

// PLP Framework Initialization
void plp_init_functor(coordinate_functor_t* functor) {
    functor->to_polar = cartesian_to_polar;
    functor->to_cartesian = polar_to_cartesian;
    functor->cartesian_add = add_cartesian_points;
    functor->polar_add = add_polar_points;
}

// Binary encoding for Cartesian coordinates (2-bit uniform representation)
uint8_t encode_cartesian_binary(double x, double y) {
    // Encode x and y into 4 bits each (0-15 range normalized)
    uint8_t x_encoded = (uint8_t)((x + 10.0) / 20.0 * 15.0);  // Map -10 to +10 range
    uint8_t y_encoded = (uint8_t)((y + 10.0) / 20.0 * 15.0);
    
    return (x_encoded << 4) | y_encoded;
}

// Binary encoding for Polar coordinates (2-bit uniform representation)  
uint8_t encode_polar_binary(double r, double theta) {
    // Encode radius (0-10 range) and angle (0-360 degrees)
    uint8_t r_encoded = (uint8_t)(r / 10.0 * 15.0);
    uint8_t theta_encoded = (uint8_t)(theta / 360.0 * 15.0);
    
    return (r_encoded << 4) | theta_encoded;
}

// Decode binary back to Cartesian
void decode_cartesian_binary(uint8_t bits, double* x, double* y) {
    uint8_t x_encoded = (bits >> 4) & 0x0F;
    uint8_t y_encoded = bits & 0x0F;
    
    *x = (x_encoded / 15.0) * 20.0 - 10.0;
    *y = (y_encoded / 15.0) * 20.0 - 10.0;
}

// Decode binary back to Polar
void decode_polar_binary(uint8_t bits, double* r, double* theta) {
    uint8_t r_encoded = (bits >> 4) & 0x0F;
    uint8_t theta_encoded = bits & 0x0F;
    
    *r = (r_encoded / 15.0) * 10.0;
    *theta = (theta_encoded / 15.0) * 360.0;
}

// Heterogeneous Functor: Cartesian to Polar conversion
polar_point_t cartesian_to_polar(cartesian_point_t cart) {
    double x, y;
    decode_cartesian_binary(cart.x_bits, &x, &y);
    
    // Convert to polar coordinates
    double r = sqrt(x*x + y*y);
    double theta = atan2(y, x) * 180.0 / M_PI;  // Convert to degrees
    
    if (theta < 0) theta += 360.0;  // Normalize to 0-360
    
    polar_point_t polar;
    polar.r_bits = encode_polar_binary(r, theta);
    polar.theta_bits = 0;  // Not used in this encoding
    
    return polar;
}

// Heterogeneous Functor: Polar to Cartesian conversion
cartesian_point_t polar_to_cartesian(polar_point_t polar) {
    double r, theta;
    decode_polar_binary(polar.r_bits, &r, &theta);
    
    // Convert to Cartesian coordinates
    double rad = theta * M_PI / 180.0;  // Convert to radians
    double x = r * cos(rad);
    double y = r * sin(rad);
    
    cartesian_point_t cart;
    cart.x_bits = encode_cartesian_binary(x, y);
    cart.y_bits = 0;  // Not used in this encoding
    
    return cart;
}

// Homogeneous Functor: Add Cartesian points
cartesian_point_t add_cartesian_points(cartesian_point_t a, cartesian_point_t b) {
    double x1, y1, x2, y2;
    decode_cartesian_binary(a.x_bits, &x1, &y1);
    decode_cartesian_binary(b.x_bits, &x2, &y2);
    
    cartesian_point_t result;
    result.x_bits = encode_cartesian_binary(x1 + x2, y1 + y2);
    result.y_bits = 0;
    
    return result;
}

// Sparse Geometry Validation
int is_sparse_mapping_valid(cartesian_point_t cart, polar_point_t polar) {
    // Convert both to Cartesian and check if they're close
    cartesian_point_t converted = polar_to_cartesian(polar);
    
    double x1, y1, x2, y2;
    decode_cartesian_binary(cart.x_bits, &x1, &y1);
    decode_cartesian_binary(converted.x_bits, &x2, &y2);
    
    double distance = sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
    return distance < 1.0;  // Tolerance threshold
}

// Sparse Distance Calculation
double calculate_sparse_distance(cartesian_point_t a, cartesian_point_t b) {
    double x1, y1, x2, y2;
    decode_cartesian_binary(a.x_bits, &x1, &y1);
    decode_cartesian_binary(b.x_bits, &x2, &y2);
    
    return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
}
