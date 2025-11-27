#!/usr/bin/env python3
import hashlib

# Use the same constants as sparse_exit.py
BLOOM_BITS = 128 * 8           # 1024 bits (128 bytes)
BLOOM_BYTES = BLOOM_BITS // 8  # 128 B

def bloom_hash(x, i):
    return int.from_bytes(hashlib.sha256(f"{x}:{i}".encode()).digest()[:4], 'little') % BLOOM_BITS

bf = bytearray(BLOOM_BYTES)
edges = [('0','1'),('0','2'),('1','3'),('2','3'),('3','4')]

for a, b in edges:
    for i in range(3):
        idx = bloom_hash((a, b), i)
        bf[idx // 8] |= 1 << (idx % 8)

with open('hints.bin', 'wb') as f:
    f.write(bf)

print(f"Created hints.bin with {len(bf)} bytes")
print(f"File should contain Bloom filter for edges: {edges}")
