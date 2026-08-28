"""
Benchmark scaling of the superstring spectrum computation to higher levels.
"""

import time
from collections import defaultdict
from test_spectrum import (
    compute_fock_levels, poly_div_susy, decompose_so8_char,
    decompose_so8_to_so9, decompose_so9_to_so10
)

def benchmark(max_level=16):
    print(f"{'Level':<6} {'Fock Terms':<12} {'Fock Time':<10} {'Div Time':<10} {'SO8 Invert':<10} {'SO9 Invert':<10} {'SO10 Solve':<10} {'Total':<10}")
    print("-" * 80)
    
    t0 = time.time()
    F = compute_fock_levels(max_level)
    fock_total_time = time.time() - t0
    
    r_so9_list = [None]
    
    for l in range(1, max_level + 1):
        t_l0 = time.time()
        
        # 1. Poly div
        t_div0 = time.time()
        Q = poly_div_susy(F[l])
        t_div = time.time() - t_div0
        
        # 2. SO8 Invert
        t_so8_0 = time.time()
        so8_m = decompose_so8_char(Q)
        t_so8 = time.time() - t_so8_0
        
        # 3. SO9 Invert
        t_so9_0 = time.time()
        so9_m = decompose_so8_to_so9(so8_m)
        t_so9 = time.time() - t_so9_0
        r_so9_list.append(so9_m)
        
        # 4. SO10 Solve for cumulative
        so9_cum = defaultdict(int)
        for k in range(1, l + 1):
            for h, m in r_so9_list[k].items():
                so9_cum[h] += m
        t_so10_0 = time.time()
        so10_m = decompose_so9_to_so10(so9_cum)
        t_so10 = time.time() - t_so10_0
        
        t_total = time.time() - t_l0
        num_terms = len(F[l])
        
        print(f"{l:<6d} {num_terms:<12d} {fock_total_time if l==1 else 0:<10.3f} {t_div:<10.3f} {t_so8:<10.3f} {t_so9:<10.3f} {t_so10:<10.3f} {t_total:<10.3f}")

if __name__ == "__main__":
    benchmark(14)
