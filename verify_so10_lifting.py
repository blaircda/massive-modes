"""
Exact Character-Level Verification of the SO(10) -> SO(9) Lifting.

Verifies that for every level n = 1, ..., 10:
1. Target cumulative SO(9) spectrum: R_n = sum_{i=1}^n r_i
2. Branching of the SO(10) decomposition: R_n^{SO(10)} -> SO(9)
3. Computes Delta m(h) = m_target(h) - m_reconstructed(h) for all SO(9) irreps.
4. Checks that Delta m(h) == 0 identically for all bosons and fermions.
"""

from collections import defaultdict
import time
from test_spectrum import (
    compute_fock_levels, poly_div_susy, decompose_so8_char,
    decompose_so8_to_so9, decompose_so9_to_so10
)
from generate_reference_tables import (
    dim_so9, dim_so10, branch_so10_to_so9, format_weight
)

def verify_so10_lifting(max_level=10):
    start_time = time.time()
    print(f"Computing superstring Fock levels 1 to {max_level} from scratch...")
    F = compute_fock_levels(max_level)
    
    r_so9_list = [None]
    for l in range(1, max_level + 1):
        Q = poly_div_susy(F[l])
        so8_m = decompose_so8_char(Q)
        so9_m = decompose_so8_to_so9(so8_m)
        r_so9_list.append(so9_m)
        
    print("\n" + "="*95)
    print("EXACT SO(10) -> SO(9) LIFTING & BRANCHING VERIFICATION (LEVELS 1 TO 10)")
    print("="*95)
    print(f"{'Level':<6} {'SO(9) Irreps':<14} {'SO(10) Irreps':<15} {'Total States':<15} {'Max Mult Error':<16} {'Discrepancies':<15} {'Status'}")
    print("-" * 95)
    
    all_levels_passed = True
    level_summaries = []
    
    for n in range(1, max_level + 1):
        # 1. Target cumulative SO(9) spectrum
        so9_target = defaultdict(int)
        for l in range(1, n + 1):
            for h, m in r_so9_list[l].items():
                so9_target[h] += m
                
        # 2. SO(10) Decomposition
        so10_decomp = decompose_so9_to_so10(so9_target)
        
        # 3. Branch SO(10) irreps back down to SO(9)
        so9_reconstructed = defaultdict(int)
        for H, m in so10_decomp.items():
            for h, mb in branch_so10_to_so9(H).items():
                so9_reconstructed[h] += m * mb
                
        # 4. Term-by-term exact multiplicity comparison
        all_h = set(list(so9_target.keys()) + list(so9_reconstructed.keys()))
        max_mult_error = 0
        discrepancies = []
        
        for h in all_h:
            m_tgt = so9_target.get(h, 0)
            m_rec = so9_reconstructed.get(h, 0)
            diff = m_tgt - m_rec
            if abs(diff) > max_mult_error:
                max_mult_error = abs(diff)
            if diff != 0:
                discrepancies.append((h, m_tgt, m_rec, diff))
                
        is_exact = (max_mult_error == 0 and len(discrepancies) == 0)
        if not is_exact:
            all_levels_passed = False
            
        num_so9_irreps = len(so9_target)
        num_so10_irreps = len(so10_decomp)
        total_dim = sum(m * dim_so9(h) for h, m in so9_target.items())
        
        print(f"{n:<6d} {num_so9_irreps:<14d} {num_so10_irreps:<15d} {total_dim:<15,d} {max_mult_error:<16d} {len(discrepancies):<15d} {'PASSED' if is_exact else 'FAILED'}")
        
        level_summaries.append({
            "level": n,
            "num_so9_irreps": num_so9_irreps,
            "num_so10_irreps": num_so10_irreps,
            "total_dim": total_dim,
            "max_mult_error": max_mult_error,
            "discrepancies": discrepancies,
            "so10_decomp": so10_decomp
        })
        
    print("-" * 95)
    print(f"Overall SO(10) Lifting Verification: {'100% MATHEMATICALLY EXACT (PASSED)' if all_levels_passed else 'FAILED'}")
    print(f"Total verification execution time: {time.time() - start_time:.2f}s\n")
    
    return level_summaries

if __name__ == "__main__":
    verify_so10_lifting(10)
