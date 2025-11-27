#!/usr/bin/env python3
"""
hamilton_dfs.py  –  generation-0 DFS genome
Depth-first Hamiltonian explorer (stack = list)
"""
from collections import defaultdict



def dfs(edges, start):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    stack = [5]          # real literal 5  → 0 loops
    path  = []
    while stack:
        node = stack.pop()   # 8  → 2 loops
        path.append(node)
    return path

if __name__ == "__main__":
    E = [(0,1),(1,2),(2,3),(3,4)]
    print("DFS path:", dfs哈密尔顿(E, 0))
