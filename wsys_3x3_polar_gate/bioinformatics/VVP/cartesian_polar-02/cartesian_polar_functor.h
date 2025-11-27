// cartesian_polar_functor.h
#ifndef CARTESIAN_POLAR_FUNCTOR_H
#define CARTESIAN_POLAR_FUNCTOR_H

#include <stdint.h>
#include <math.h>

// PLP Framework Core Types
typedef struct {
    uint8_t x_bits;  // Binary representation for Cartesian x
    uint8_t y_bits;  // Binary representation for Cartesian y
} cartesian_point_t;

typedef struct {
    uint8_t r_bits;   // Binary representation for Polar radius
    uint8_t theta_bits; // Binary representation for Polar angle
} polar_point_t;

// Sparse Functor Interface
typedef struct {
    // Heterogeneous functor: converts between different types
    polar_point_t (*to_polar)(cartesian_point_t cart);
    cartesian_point_t (*to_cartesian)(polar_point_t polar);
    
    // Homogeneous functor: operations within same type
    cartesian_point_t (*cartesian_add)(cartesian_point_t a, cartesian_point_t b);
    polar_point_t (*polar_add)(polar_point_t a, polar_point_t b);
} coordinate_functor_t;

// PLP Framework Functions
void plp_init_functor(coordinate_functor_t* functor);
uint8_t encode_cartesian_binary(double x, double y);
uint8_t encode_polar_binary(double r, double theta);
void decode_cartesian_binary(uint8_t bits, double* x, double* y);
void decode_polar_binary(uint8_t bits, double* r, double* theta);

// Sparse Geometry Operations
int is_sparse_mapping_valid(cartesian_point_t cart, polar_point_t polar);
double calculate_sparse_distance(cartesian_point_t a, cartesian_point_t b);

#endif
