#!/usr/bin/env python3
"""
hamilton_sync_functor.py — FIXED & UNIFIED
Nnamdi Michael Okpala — OBINexus — Nov 27 2025
Sparse dynamic sync: DFS ↔ BFS genomes → isomorphic 95.4% coherence
With EE override + 00-veto + hints.bin oracle
"""
import ast
import copy
import pathlib
import sys
import math

TARGET = 0.954
LOOP_COUNT = [1, 0, 0, 0, 0, 0, 1, 0, 2, 1]  # 0-9 closed loops (your sparse geometry)
SHAPE_QUEUE = ast.Name(id='deque', ctx=ast.Load())  # BFS shape
SHAPE_STACK = ast.Name(id='list', ctx=ast.Load())   # DFS shape
HINTS_FILE = "hints.bin"  # your sparse_exit-01 oracle

# ---------- 1. Coherence Oracle (95.4% target) -------------------------
def coherence(tree: ast.AST) -> float:
    nums = [node.n for node in ast.walk(tree) if isinstance(node, ast.Num)]
    if not nums: return 0.0
    return sum(LOOP_COUNT[n % 10] for n in nums) / len(nums)

# ---------- 2. Canonical Digit (sparse local min/max) -------------------
def canon_num(node: ast.Num):
    want = LOOP_COUNT[node.n % 10]
    for cand in range(10):
        if LOOP_COUNT[cand] == want:
            node.n = cand
            return

# ---------- 3. Force Shape + EE Override (policy switch) ----------------
def force_shape(tree: ast.Module, target_shape: ast.Name, override: str = None) -> ast.Module:
    mutant = copy.deepcopy(tree)
    for node in ast.walk(mutant):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('deque', 'list'):
                node.func = target_shape
        if isinstance(node, ast.Num):
            canon_num(node)
        # EE emergency: Force connect if override
        if override == "EE":
            # Inject emergency functor — bypass veto
            node.n = 14  # 1+4=5, but %10=4 → LOOP[4]=0 (silence to connect)
    return mutant

# ---------- 4. Load Genomes + Hints Oracle ------------------------------
def load_genome(p: pathlib.Path) -> ast.Module:
    return ast.parse(p.read_text())

def load_hints():
    try:
        with open(HINTS_FILE, "rb") as f:
            data = f.read()
            # Sparse pairs from hints.bin (your bio-informatics coherence)
            pairs = list(zip(data[::2], data[1::2]))
            return pairs
    except FileNotFoundError:
        return []  # ε0000 silence — pre-birth

def flash_genome(tree: ast.Module, out_p: pathlib.Path):
    out_p.write_text(ast.unparse(tree))

# ---------- 5. Sparse Dynamic Consensus Switch (Your Spoken Law) --------
class SparseSwitch:
    def __init__(self):
        self.epsilon = 0b0000  # ε0000 pre-birth
        self.hints_pairs = load_hints()  # bio-informatics oracle
        self.coherence_pairs = []  # AND-constrained (00/11 only)

    def derive(self, input_ast: ast.Module, override: str = None) -> str:
        if override == "EE":  # Emergency force-connect
            return "CONNECT"  # Bypass veto — rainforest lifeline
        if self.epsilon == 0b0000:  # 00-veto
            return "REJECT"  # Absolute NO
        if self.check_pairs(input_ast):
            return "EXECUTE"  # 11 full sync
        return "SWITCH"  # if-then-else → change path (Claude enforce)

    def check_pairs(self, ast_tree: ast.Module) -> bool:
        # AND-constrained: only 00, 11, EE pairs pass
        nums = [node.n for node in ast.walk(ast_tree) if isinstance(node, ast.Num)]
        for i in range(0, len(nums), 2):
            a, b = nums[i] & 0xF, nums[i+1] & 0xF if i+1 < len(nums) else 0
            pair = (a, b)
            if pair not in [(0,0), (1,1), (0xE,0xE)]:  # 00, 11, EE
                return False
        return True

# ---------- 6. MAIN — Sync DFS/BFS Genomes -------------------------------
def main():
    repo = pathlib.Path(__file__).parent
    dfs_p = repo / 'hamilton_dfs.py'
    bfs_p = repo / 'hamilton_bfs.py'
    out_p = repo / 'hamilton_sync.py'

    dfs_ast = load_genome(dfs_p)
    bfs_ast = load_genome(bfs_p)

    print(f"pre-sync coherence DFS={coherence(dfs_ast):.3f} BFS={coherence(bfs_ast):.3f}")

    # Sparse switch policy
    switch = SparseSwitch()
    policy = switch.derive(dfs_ast)  # Derive from input
    print(f"Policy: {policy}")

    # Force canonical shape (if-then-else negotiation)
    dfs_ast = force_shape(dfs_ast, SHAPE_QUEUE)
    bfs_ast = force_shape(bfs_ast, SHAPE_QUEUE)

    # Unify (isomorphic merge)
    unified = copy.deepcopy(dfs_ast)
    unified.body.extend(bfs_ast.body)

    # Evolve to 95.4% (sparse dynamic loop)
    best = unified
    for _ in range(500):
        if coherence(best) >= TARGET:
            break
        challenger = copy.deepcopy(best)
        for node in ast.walk(challenger):
            if isinstance(node, ast.Num):
                node.n = (node.n + 1) % 10  # Rotate literals
        if coherence(challenger) > coherence(best):
            best = challenger

    # Flash unified genome
    flash_genome(best, out_p)
    print(f"post-sync coherence = {coherence(best):.3f} → flashed to {out_p}")

if __name__ == "__main__":
    main()
