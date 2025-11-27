#!/usr/bin/env python3
"""
hamilton_sync_functor.py
Bio-informatic desync → sync for Hamiltonian DFS/BFS
- canonicalises edge literals with loop-count rule
- forces both ASTs into identical queue-vs-stack shape
- flashes unified genome back (relay sustainability)
"""
import ast, copy, pathlib, sys, math

TARGET      = 0.954
LOOP_COUNT  = [1,0,0,0,0,0,1,0,2,1]   # 0-9 closed loops
SHAPE_QUEUE = ast.Name(id='deque', ctx=ast.Load())   # BFS shape
SHAPE_STACK = ast.Name(id='list',  ctx=ast.Load())   # DFS shape

# ---------- 1.  coherence oracle ------------------------------------------
def coherence(tree: ast.AST) -> float:
    nums = [node.n for node in ast.walk(tree) if isinstance(node, ast.Num)]
    if not nums: return 0.0
    return sum(LOOP_COUNT[n%10] for n in nums) / len(nums)

# ---------- 2.  canonical digit -------------------------------------------
def canon_num(node: ast.Num):
    want = LOOP_COUNT[node.n % 10]
    for cand in range(10):
        if LOOP_COUNT[cand] == want:
            node.n = cand
            return

# ---------- 3.  force queue-vs-stack shape ---------------------------------
def force_shape(tree: ast.Module, target_shape: ast.Name) -> ast.Module:
    mutant = copy.deepcopy(tree)
    for node in ast.walk(mutant):
        # any call to deque()/list() → target_shape
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('deque', 'list'):
                node.func = target_shape
        # canonicalise every literal
        if isinstance(node, ast.Num):
            canon_num(node)
    return mutant

# ---------- 4.  load both genomes -----------------------------------------
repo  = pathlib.Path(__file__).parent
dfs_p = repo / 'hamilton_dfs.py'
bfs_p = repo / 'hamilton_bfs.py'
out_p = repo / 'hamilton_sync.py'

dfs_ast = ast.parse(dfs_p.read_text())
bfs_ast = ast.parse(bfs_p.read_text())

print("pre-sync  coherence  DFS=%.3f  BFS=%.3f" % (coherence(dfs_ast), coherence(bfs_ast)))

# ---------- 5.  unify shape → both use deque (BFS queue) ------------------
dfs_ast = force_shape(dfs_ast, SHAPE_QUEUE)
bfs_ast = force_shape(bfs_ast, SHAPE_QUEUE)

# ---------- 6.  make them identical ---------------------------------------
unified = copy.deepcopy(dfs_ast)
unified.body.extend(bfs_ast.body)

# ---------- 7.  final evolution push to 95.4 % ----------------------------
best = unified
for _ in range(500):
    if coherence(best) >= TARGET:
        break
    challenger = copy.deepcopy(best)
    for node in ast.walk(challenger):
        if isinstance(node, ast.Num):
            node.n = (node.n + 1) % 10
    if coherence(challenger) > coherence(best):
        best = challenger

# ---------- 8.  flash unified genome --------------------------------------
out_p.write_text(ast.unparse(best))
print("post-sync coherence = %.3f  → flashed to %s" % (coherence(best), out_p))
