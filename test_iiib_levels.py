"""
Test Proposal III.B up to Level 10.
Proposal III.B: R^{(n)} = sum_{l=1}^n r^{(l)} forms valid non-negative SO(10) representations.
"""

from collections import defaultdict
import time
from test_spectrum import (
    compute_fock_levels, poly_div_susy, decompose_so8_char,
    decompose_so8_to_so9, decompose_so9_to_so10, branch_so10_to_so9
)

def dim_so10(H):
    l = [H[0]+4, H[1]+3, H[2]+2, H[3]+1, H[4]]
    num = 1
    for i in range(5):
        for j in range(i+1, 5):
            num *= (l[i] - l[j]) * (l[i] + l[j])
    den = 1
    rho = [4, 3, 2, 1, 0]
    for i in range(5):
        for j in range(i+1, 5):
            den *= (rho[i] - rho[j]) * (rho[i] + rho[j])
    return int(round(abs(num) / den))

MAX_L = 10
print(f"Computing string spectrum up to Level {MAX_L}...")
t0 = time.time()
F = compute_fock_levels(MAX_L)
print(f"Fock space computed in {time.time()-t0:.2f}s")

r_so9_list = [None]
for l in range(1, MAX_L + 1):
    t_l = time.time()
    Q = poly_div_susy(F[l])
    so8_m = decompose_so8_char(Q)
    so9_m = decompose_so8_to_so9(so8_m)
    r_so9_list.append(so9_m)
    print(f"Level {l} computed in {time.time()-t_l:.2f}s (num SO(9) irreps: {len(so9_m)})")

print("\n" + "="*80)
print("TESTING PROPOSAL III.B (CUMULATIVE SPECTRUM sum_{l=1}^n r^{(l)}) FOR LEVELS 1 TO 10")
print("="*80)

results = []

for n in range(1, MAX_L + 1):
    t_start = time.time()
    so9_cum = defaultdict(int)
    for l in range(1, n + 1):
        for h, m in r_so9_list[l].items():
            so9_cum[h] += m
            
    d_so10 = decompose_so9_to_so10(so9_cum)
    neg_reps = {H: m for H, m in d_so10.items() if m < 0}
    pos_reps = {H: m for H, m in d_so10.items() if m > 0}
    
    passed = (len(neg_reps) == 0)
    elapsed = time.time() - t_start
    results.append((n, passed, pos_reps, neg_reps, elapsed))
    
    status_str = "PASSED [All non-negative]" if passed else f"FAILED [Negative multiplicities: {len(neg_reps)}]"
    print(f"\nLevel n = {n}: {status_str} (solved in {elapsed:.3f}s)")
    
    # Print decomposition breakdown
    bosons = {H: m for H, m in pos_reps.items() if abs(H[0] - int(H[0])) < 0.1}
    fermions = {H: m for H, m in pos_reps.items() if abs(H[0] - int(H[0])) > 0.1}
    
    print("  Bosonic SO(10) irreps:")
    for H, m in sorted(bosons.items(), key=lambda x: -dim_so10(x[0])):
        print(f"    mult {m} x {H} (dim {dim_so10(H)})")
    print("  Fermionic SO(10) irreps:")
    for H, m in sorted(fermions.items(), key=lambda x: -dim_so10(x[0])):
        print(f"    mult {m} x {H} (dim {dim_so10(H)})")
        
    if neg_reps:
        print("  Negative multiplicity irreps:")
        for H, m in sorted(neg_reps.items()):
            print(f"    mult {m} x {H} (dim {dim_so10(H)})")

print("\n" + "="*80)
print("FINAL SUMMARY FOR PROPOSAL III.B")
print("="*80)
for n, passed, _, negs, el in results:
    res = "PASSED" if passed else f"FAILED ({len(negs)} negative irreps)"
    print(f"Level {n:2d}: {res:<35} ({el:.3f}s)")
