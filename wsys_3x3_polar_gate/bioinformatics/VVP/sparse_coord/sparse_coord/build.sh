#!/usr/bin/env bash
set -e
gcc -Wall -O2 -fPIC -shared plp128.c -lm -o plp128.so
echo "plp128.so built successfully"

gcc -O2 demo_cart2pol.c plp128.so -lm -o demo
./demo
# r = 13.000000  θ = 22.619865°
