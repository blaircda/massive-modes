"""
Summarize Level 6 in Bosonic and Fermionic sectors.
"""

from collections import defaultdict
from test_spectrum import (
    r_so9_list, decompose_so9_to_so10, branch_so10_to_so9
)
from test_iiic import get_partitions

# Dimensions of SO(9) and SO(10) irreps using Weyl dimension formula
def dim_so9(h):
    # h = (h1, h2, h3, h4)
    # rho = (7/2, 5/2, 3/2, 1/2)
    rho = [3.5, 2.5, 1.5, 0.5]
    l = [h[i] + rho[i] for i in range(4)]
    # positive roots of B4: e_i (4 roots), e_i +- e_j (12 roots)
    prod = 1.0
    # e_i roots: l_i / rho_i
    for i in range(4):
        prod *= (l[i] / rho[i])
    # e_i +- e_j roots
    for i in range(4):
        for j in range(i+1, 4):
            prod *= (l[i] - l[j]) / (rho[i] - rho[j])
            prod *= (l[i] + l[j]) / (rho[i] + rho[j])
    return int(round(prod))

def dim_so10(H):
    # H = (H1, H2, H3, H4, H5)
    # rho = (4, 3, 2, 1, 0)
    rho = [4.0, 3.0, 2.0, 1.0, 0.0]
    l = [H[i] + rho[i] for i in range(5)]
    # positive roots of D5: e_i +- e_j (20 roots)
    prod = 1.0
    for i in range(5):
        for j in range(i+1, 5):
            prod *= (l[i] - l[j]) / (rho[i] - rho[j])
            prod *= (l[i] + l[j]) / (rho[i] + rho[j])
    return int(round(prod))

def is_fermionic(hw):
    return (abs(hw[0] - int(hw[0])) > 0.1)

# Level 6 perturbative r^(6)
r6 = r_so9_list[6]
r6_B = {h: m for h, m in r6.items() if not is_fermionic(h)}
r6_F = {h: m for h, m in r6.items() if is_fermionic(h)}

print("=== LEVEL 6 PERTURBATIVE SPECTRUM r^(6) ===")
print("Bosons in r^(6):")
for h, m in sorted(r6_B.items(), key=lambda x: -dim_so9(x[0])):
    print(f"  SO(9) {h} (dim {dim_so9(h)}): mult {m}")
print(f"Total bosonic dim in r^(6): {sum(dim_so9(h)*m for h, m in r6_B.items())}")

print("\nFermions in r^(6):")
for h, m in sorted(r6_F.items(), key=lambda x: -dim_so9(x[0])):
    print(f"  SO(9) {h} (dim {dim_so9(h)}): mult {m}")
print(f"Total fermionic dim in r^(6): {sum(dim_so9(h)*m for h, m in r6_F.items())}")

# Proposal III.B at level 6
cum6 = defaultdict(int)
for l in range(1, 7):
    for h, m in r_so9_list[l].items():
        cum6[h] += m

decomp6_B = decompose_so9_to_so10({h: m for h, m in cum6.items() if not is_fermionic(h)})
decomp6_F = decompose_so9_to_so10({h: m for h, m in cum6.items() if is_fermionic(h)})

print("\n" + "="*60)
print("PROPOSAL III.B (Level 6) SO(10) DECOMPOSITION")
print("="*60)
print("Bosonic Sector:")
for H, m in sorted(decomp6_B.items(), key=lambda x: -dim_so10(x[0])):
    status = " [NEGATIVE!]" if m < 0 else ""
    print(f"  SO(10) {H} (dim {dim_so10(H)}): mult {m}{status}")

print("\nFermionic Sector:")
for H, m in sorted(decomp6_F.items(), key=lambda x: -dim_so10(x[0])):
    status = " [NEGATIVE!]" if m < 0 else ""
    print(f"  SO(10) {H} (dim {dim_so10(H)}): mult {m}{status}")

# Proposal III.C at level 6
p = get_partitions(6)
cum6_c = defaultdict(int)
for l in range(1, 7):
    w = p[6 - l]
    for h, m in r_so9_list[l].items():
        cum6_c[h] += w * m

decomp6_c_B = decompose_so9_to_so10({h: m for h, m in cum6_c.items() if not is_fermionic(h)})
decomp6_c_F = decompose_so9_to_so10({h: m for h, m in cum6_c.items() if is_fermionic(h)})

print("\n" + "="*60)
print("PROPOSAL III.C (Level 6) SO(10) DECOMPOSITION")
print("="*60)
print("Bosonic Sector:")
for H, m in sorted(decomp6_c_B.items(), key=lambda x: -dim_so10(x[0])):
    status = " [NEGATIVE!]" if m < 0 else ""
    print(f"  SO(10) {H} (dim {dim_so10(H)}): mult {m}{status}")

print("\nFermionic Sector:")
for H, m in sorted(decomp6_c_F.items(), key=lambda x: -dim_so10(x[0])):
    status = " [NEGATIVE!]" if m < 0 else ""
    print(f"  SO(10) {H} (dim {dim_so10(H)}): mult {m}{status}")
