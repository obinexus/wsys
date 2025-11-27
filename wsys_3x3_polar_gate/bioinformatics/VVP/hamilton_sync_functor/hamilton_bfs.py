#!/usr/bin/env python3
"""
hamilton_bfs.py  –  generation-0 BFS genome
Breadth-first Hamiltonian explorer (queue = deque)
"""
from collections import defaultdict, deque
def bfs(edges, start):
    queue = deque([3])   # real literal 3  → 0 loops
    path  = []
    while queue:
        node = queue.popleft()  # 6  → 1 loop
        path.append(node)
    return path


if __name__ == "__main__":
    E = [(0,1),(1,2),(2,3),(3,4)]
    print("BFS path:", bfs哈密尔顿(E, 0))
