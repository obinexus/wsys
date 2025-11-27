#!/usr/bin/env python3
"""
sparse_coord.py  –  PLP sparse functor for Cartesian ⇄ Polar
usage:
    python sparse_coord.py cart 12 5
    python sparse_coord.py pol 13 22.62
"""
import os, struct, json, math, hashlib, sys

BLOOM_BYTES = 128
BLOOM_BITS  = BLOOM_BYTES * 8

def bloom_hash(x: tuple, i: int) -> int:
    return int.from_bytes(
        hashlib.sha256(f"{x}:{i}".encode()).digest()[:4], 'little'
    ) % BLOOM_BITS

def bloom_set(bf: bytearray, x: tuple):
    for i in range(3):
        idx = bloom_hash(x, i)
        bf[idx//8] |= 1 << (idx % 8)

def bloom_check(bf: bytes, x: tuple) -> bool:
    return all(
        bf[bloom_hash(x, i)//8] & (1 << (bloom_hash(x, i) % 8))
        for i in range(3)
    )

# ---------- PLP functor ----------
TOKEN_CART, TOKEN_POL = b'\x10', b'\x01'   # 2-bit bio-tokens

class PLPFunctor:
    def __init__(self, bloom_path='hints.bin'):
        if not os.path.exists(bloom_path):
            self._bootstrap(bloom_path)
        with open(bloom_path, 'rb') as f:
            self.bloom = f.read(BLOOM_BYTES)

    @staticmethod
    def _bootstrap(path):
        bf = bytearray(BLOOM_BYTES)
        # register both directions for a tiny grid – sparse!
        for x, y in ((0,0),(1,1),(12,5)):
            r, t = math.hypot(x,y), math.degrees(math.atan2(y,x))
            bloom_set(bf, (TOKEN_CART, x, y, round(r,2), round(t,2)))
            bloom_set(bf, (TOKEN_POL, round(r,2), round(t,2), x, y))
        with open(path, 'wb') as f:
            f.write(bf)

    def apply(self, token: bytes, *args):
        key = (token, *args)
        if not bloom_check(self.bloom, key):
            raise RuntimeError('PLP: sparse key not registered – use wider bootstrap')
        if token == TOKEN_CART:
            x, y = args
            r, theta = math.hypot(x,y), math.degrees(math.atan2(y,x))
            return round(r,2), round(theta,2)
        else:  # POL
            r, theta = args
            rad = math.radians(theta)
            return round(r*math.cos(rad),2), round(r*math.sin(rad),2)

# ---------- CLI ----------
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(1)
    mode, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    fun = PLPFunctor()
    if mode == 'cart':
        r, t = fun.apply(TOKEN_CART, a, b)
        print(f'Polar=({r}, {t}°)')
    elif mode == 'pol':
        x, y = fun.apply(TOKEN_POL, a, b)
        print(f'Cartesian=({x}, {y})')
    else:
        print('mode ∈ {cart, pol}')
