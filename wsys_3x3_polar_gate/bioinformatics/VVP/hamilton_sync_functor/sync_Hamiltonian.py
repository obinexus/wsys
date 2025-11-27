#!/usr/bin/env python3
"""
sync Hamiltonian.py
Bio-informatic de-synchronisation → synchronisation engine
- canonicalises two divergent ASTs until they are isomorphic
- coherence target = 95.4 % (loop-count of every int literal)
- flashes the unified genome back to disk (relay sustainability)
"""
import ast, copy, pathlib, sys, math

TARGET = 0.954
LOOP     = [1,0,0,0,0,0,1,0,2,1]   # 0-9 closed loops

# ---------- 1.  coherence oracle ------------------------------------------
def coherence(tree: ast.AST) -> float:
    nums = [node.n for node in ast.walk(tree) if isinstance(node, ast.Num)]
    if not nums: return 0.0
    return sum(LOOP[n%10] for n in nums) / len(nums)

# ---------- 2.  canonicalise one literal ----------------------------------
def canon_num(node: ast.Num):
    """Map any literal → canonical digit with same loop-count"""
    want = LOOP[node.n % 10]
    for cand in range(10):
        if LOOP[cand] == want:
            node.n = cand
            return

# ---------- 3.  force whole AST into canonical shape ----------------------
def canon_tree(tree: ast.Module) -> ast.Module:
    mutant = copy.deepcopy(tree)
    for node in ast.walk(mutant):
        if isinstance(node, ast.Num):
            canon_num(node)
    return mutant

# ---------- 4.  load both divergent genomes -------------------------------
def load(p: pathlib.Path) -> ast.Module:
    return ast.parse(p.read_text())

def flash(tree: ast.Module, p: pathlib.Path):
    p.write_text(ast.unparse(tree))

# ---------- 5.  main --------------------------------------------------------
def main():
    repo   = pathlib.Path(__file__).parent
    dfs_py = repo / "hamilton_dfs.py"   # depth-first (recursive) version
    bfs_py = repo / "hamilton_bfs.py"   # breadth-first (queue) version
    out_py = repo / "hamilton_sync.py"  # unified, coherent genome

    dfs_ast = load(dfs_py)
    bfs_ast = load(bfs_py)

    print("pre-sync  coherence  DFS=%.3f  BFS=%.3f" %
          (coherence(dfs_ast), coherence(bfs_ast)))

    # force both into canonical shape
    dfs_ast = canon_tree(dfs_ast)
    bfs_ast = canon_tree(bfs_ast)

    # make them identical (isomorphic)
    unified = copy.deepcopy(dfs_ast)
    unified.body.extend(bfs_ast.body)

    # final evolution step – raise coherence to 95.4 %
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

    flash(best, out_py)
    print("post-sync coherence = %.3f  → flashed to %s" % (coherence(best), out_py))

if __name__ == "__main__":
    main()
