#!/usr/bin/env bash
set -euo pipefail

echo "=== PLP-128 Build Audit (Neurodivergent-First) ==="
echo "OS: $(uname -s)"
echo "GCC: $(gcc --version | head -1)"

# Build
mkdir -p sparse_coord/lib sparse_coord/include

# Ensure header
if [ ! -f sparse_coord/include/plp128.h ]; then
    cat > sparse_coord/include/plp128.h << 'EOF'
#ifndef PLP128_H
#define PLP128_H
#include <stdint.h>
void plp_load(const uint8_t *bloom128);
int plp_cart2pol(double x, double y, double out[2]);
int plp_pol2cart(double r, double theta_deg, double out[2]);
#endif
EOF
    echo "Created plp128.h"
fi

# Build .so
echo "Building plp128.so..."
gcc -Wall -Wextra -O2 -fPIC -shared sparse_coord/src/plp128.c -lm -o sparse_coord/lib/plp128.so

# REAL LOAD TEST
echo "Running REAL load test..."
cat > /tmp/test_plp.c << 'EOF'
#include "plp128.h"
#include <stdio.h>
int main() {
    double out[2];
    plp_cart2pol(3,4,out);
    printf("Test: r=%.1f θ=%.1f°\n", out[0], out[1]);
    return 0;
}
EOF

gcc /tmp/test_plp.c -Isparse_coord/include -Lsparse_coord/lib -lplp128 -lm -o /tmp/test_plp
if /tmp/test_plp; then
    echo "REAL LOAD TEST PASSED"
else
    echo "REAL LOAD TEST FAILED"
    exit 1
fi

rm /tmp/test_plp.c /tmp/test_plp

echo "Build COMPLETE. Library ready:"
ls -lh sparse_coord/lib/plp128.so
