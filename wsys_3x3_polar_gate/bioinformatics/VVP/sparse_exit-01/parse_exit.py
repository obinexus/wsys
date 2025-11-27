#!/usr/bin/env python3
import sys, struct, json, hashlib
from collections import defaultdict, deque

# ---------- 1. 128-byte Bloom filter helpers ----------
BLOOM_BITS = 1024 * 8          # 1 k-bit
BLOOM_BYTES = BLOOM_BITS // 8  # 128 B
def bloom_hash(x, i):
    return int.from_bytes(hashlib.sha256(f"{x}:{i}".encode()).digest()[:4], 'little') % BLOOM_BITS
def bloom_check(bf, edge):
    a, b = edge
    return all(bf[bloom_hash((a, b), i) // 8] & (1 << (bloom_hash((a, b), i) % 8)) for i in range(3))

# ---------- 2. read inputs ----------
def die(msg): print(msg, file=sys.stderr); sys.exit(1)
if len(sys.argv) != 3: die("usage: sparse_exit.py hints.bin partial.json")
with open(sys.argv[1], 'rb') as f: bloom = f.read(BLOOM_BYTES)
if len(bloom) != BLOOM_BYTES: die("hint file must be 128 B")
try:
    with open(sys.argv[2]) as f: edges = json.load(f)  # {"0":[1,2],"1":[0],...}
except Exception as e: die(f"bad json: {e}")

# ---------- 3. build undirected sparse graph ----------
G = defaultdict(list)
for u, vs in edges.items():
    for v in vs:
        if bloom_check(bloom, (u, v)):
            G[u].append(v); G[v].append(u)

# ---------- 4. greedy longest-path heuristic (DFS) ----------
def dfs_path(start):
    best = []
    def dfs(u, path, seen):
        nonlocal best
        if len(path) > len(best): best = path.copy()
        for v in G[u]:
            if v not in seen:
                seen.add(v); path.append(v)
                dfs(v, path, seen)
                path.pop(); seen.remove(v)
    dfs(start, [start], {start})
    return best

# ---------- 5. pick the longest Hamiltonian-ish chain ----------
if not G: die("NO_EXIT")
longest = max((dfs_path(n) for n in list(G)), key=len)
print(" ".join(longest))
