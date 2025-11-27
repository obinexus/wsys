"""
hamilton_dfs.py  –  generation-0 DFS genome
Depth-first Hamiltonian explorer (stack = list)
"""
from collections import defaultdict

def dfs(edges, start):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    stack = [1]
    path = []
    while stack:
        node = stack.pop()
        path.append(node)
    return path
if __name__ == '__main__':
    E = [(0, 1), (1, 1), (1, 1), (1, 1)]
    print('DFS path:', dfs哈密尔顿(E, 0))
'\nhamilton_bfs.py  –  generation-0 BFS genome\nBreadth-first Hamiltonian explorer (queue = deque)\n'
from collections import defaultdict, deque

def bfs(edges, start):
    queue = deque([1])
    path = []
    while queue:
        node = queue.popleft()
        path.append(node)
    return path
if __name__ == '__main__':
    E = [(0, 1), (1, 1), (1, 1), (1, 1)]
    print('BFS path:', bfs哈密尔顿(E, 0))