"""
Interactive Inspector and Validator for Massive String Modes and D=11 Lift.
Allows detailed inspection of any level l or cumulative level n (1 to 10).
"""

import sys
from collections import defaultdict
from test_spectrum import (
    compute_fock_levels, poly_div_susy, decompose_so8_char,
    decompose_so8_to_so9, decompose_so9_to_so10
)
from generate_reference_tables import (
    dim_so8, dim_so9, dim_so10,
    tensor_name_so8, tensor_name_so9, tensor_name_so10,
    format_weight, branch_so10_to_so9, branch_so9_to_so8
)

def inspect_single_level(l, F_l, Q_l, so8_m, so9_m):
    print("=" * 80)
    print(f"DETAILED MODE STRUCTURE FOR SINGLE LEVEL l = {l}")
    print("=" * 80)
    
    # 1. Total Fock Space & SUSY Factorization
    dim_fock_B = sum(c for w, c in F_l.items() if abs(w[0] - int(w[0])) < 0.1)
    dim_fock_F = sum(c for w, c in F_l.items() if abs(w[0] - int(w[0])) > 0.1)
    dim_r_B = sum(m * dim_so8(w) for w, m in so8_m.items() if abs(w[0] - int(w[0])) < 0.1)
    dim_r_F = sum(m * dim_so8(w) for w, m in so8_m.items() if abs(w[0] - int(w[0])) > 0.1)
    
    print("1. Fock Space & Physical State Accounting:")
    print(f"   Full GS Fock Space at level {l}: {dim_fock_B} Bosons + {dim_fock_F} Fermions (Total = {dim_fock_B + dim_fock_F})")
    print(f"   Universal massive SUSY factor:  M_susy = ((44 + 84)_B + 128_F) = (128_B + 128_F)")
    print(f"   Prefactor r^({l}) Dimension:     {dim_r_B} Bosons + {dim_r_F} Fermions")
    print(f"   Physical States: (128_B + 128_F) x ({dim_r_B}_B + {dim_r_F}_F) =")
    print(f"     -> Bosons:  128 * {dim_r_B} + 128 * {dim_r_F} = {128 * (dim_r_B + dim_r_F)}")
    print(f"     -> Fermions: 128 * {dim_r_B} + 128 * {dim_r_F} = {128 * (dim_r_B + dim_r_F)}  [N_B = N_F Exactly!]")
    print()
    
    # 2. SO(8) Decomposition of r^(l)
    print("2. SO(8) Irreducible Representation Breakdown of r^(l):")
    so8_bosons = {w: m for w, m in so8_m.items() if abs(w[0] - int(w[0])) < 0.1}
    so8_fermions = {w: m for w, m in so8_m.items() if abs(w[0] - int(w[0])) > 0.1}
    
    print("   [Bosons]:")
    for w, m in sorted(so8_bosons.items(), key=lambda x: -dim_so8(x[0])):
        print(f"     {m:2d} x {dim_so8(w):<5d} {format_weight(w):<24} {tensor_name_so8(w)}")
    print("   [Fermions]:")
    for w, m in sorted(so8_fermions.items(), key=lambda x: -dim_so8(x[0])):
        print(f"     {m:2d} x {dim_so8(w):<5d} {format_weight(w):<24} {tensor_name_so8(w)}")
    print()
    
    # 3. SO(9) Lift of r^(l)
    print("3. SO(9) Irreducible Representation Structure of r^(l):")
    so9_bosons = {w: m for w, m in so9_m.items() if abs(w[0] - int(w[0])) < 0.1}
    so9_fermions = {w: m for w, m in so9_m.items() if abs(w[0] - int(w[0])) > 0.1}
    
    print("   [Bosons]:")
    for w, m in sorted(so9_bosons.items(), key=lambda x: -dim_so9(x[0])):
        print(f"     {m:2d} x {dim_so9(w):<5d} {format_weight(w):<20} {tensor_name_so9(w)}")
    print("   [Fermions]:")
    for w, m in sorted(so9_fermions.items(), key=lambda x: -dim_so9(x[0])):
        print(f"     {m:2d} x {dim_so9(w):<5d} {format_weight(w):<20} {tensor_name_so9(w)}")
    print()

def inspect_cumulative_lift(n, r_so9_list):
    print("=" * 80)
    print(f"CUMULATIVE SPECTRUM & D=11 SO(10) LIFT (PROPOSAL III.B) FOR LEVEL n = {n}")
    print(f"Target Spectrum: R^({n}) = sum_{{l=1}}^{{{n}}} r^(l)")
    print("=" * 80)
    
    # Sum up SO(9) spectrum
    so9_cum = defaultdict(int)
    for l in range(1, n + 1):
        for h, m in r_so9_list[l].items():
            so9_cum[h] += m
            
    # Perform SO(10) decomposition
    so10_decomp = decompose_so9_to_so10(so9_cum)
    
    # Branch SO(10) back to SO(9) to verify term-by-term match
    so9_reconstructed = defaultdict(int)
    for H, m in so10_decomp.items():
        for h, mb in branch_so10_to_so9(H).items():
            so9_reconstructed[h] += m * mb
            
    # Print SO(10) Multiplet
    print("1. SO(10) Supermultiplet Decomposition:")
    so10_bosons = {H: m for H, m in so10_decomp.items() if abs(H[0] - int(H[0])) < 0.1}
    so10_fermions = {H: m for H, m in so10_decomp.items() if abs(H[0] - int(H[0])) > 0.1}
    
    print("   [Bosons]:")
    for H, m in sorted(so10_bosons.items(), key=lambda x: -dim_so10(x[0])):
        neg = " [NEGATIVE!]" if m < 0 else ""
        print(f"     {m:2d} x {dim_so10(H):<6d} {format_weight(H):<26} {tensor_name_so10(H)}{neg}")
    print("   [Fermions]:")
    for H, m in sorted(so10_fermions.items(), key=lambda x: -dim_so10(x[0])):
        neg = " [NEGATIVE!]" if m < 0 else ""
        print(f"     {m:2d} x {dim_so10(H):<6d} {format_weight(H):<26} {tensor_name_so10(H)}{neg}")
    print()
    
    # Term-by-term verification table
    print("2. Term-by-Term SO(9) Branching Verification Table:")
    print(f"{'SO(9) Irrep':<24} {'SO(9) Dim':<10} {'Target Multiplicity':<22} {'Reconstructed from SO(10)':<26} {'Match'}")
    print("-" * 90)
    all_h = sorted(set(list(so9_cum.keys()) + list(so9_reconstructed.keys())), key=lambda x: -dim_so9(x))
    all_ok = True
    for h in all_h:
        m_target = so9_cum.get(h, 0)
        m_recon = so9_reconstructed.get(h, 0)
        ok = (m_target == m_recon)
        if not ok: all_ok = False
        status = "OK" if ok else "MISMATCH!"
        print(f"{format_weight(h):<24} {dim_so9(h):<10} {m_target:<22} {m_recon:<26} {status}")
    print("-" * 90)
    print(f"Overall Level {n} Lift Verification: {'100% EXACT MATCH (PASSED)' if all_ok else 'FAILED'}")
    print()

def main():
    max_level = 10
    if len(sys.argv) > 1:
        target_level = int(sys.argv[1])
    else:
        target_level = 6
        
    print(f"Precomputing string spectrum up to level {max(target_level, 6)}...")
    F = compute_fock_levels(max(target_level, 6))
    
    r_so9_list = [None]
    r_so8_list = [None]
    Q_list = [None]
    
    for l in range(1, max(target_level, 6) + 1):
        Q = poly_div_susy(F[l])
        so8_m = decompose_so8_char(Q)
        so9_m = decompose_so8_to_so9(so8_m)
        Q_list.append(Q)
        r_so8_list.append(so8_m)
        r_so9_list.append(so9_m)
        
    inspect_single_level(target_level, F[target_level], Q_list[target_level], r_so8_list[target_level], r_so9_list[target_level])
    inspect_cumulative_lift(target_level, r_so9_list)

if __name__ == "__main__":
    main()
