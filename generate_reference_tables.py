"""
Comprehensive Representation Theory Reference and Branching Tables.
Outputs human-readable tables for SO(8), SO(9), and SO(10) representations (dim <= 4000)
and their branching rules.
"""

from collections import defaultdict
import itertools

# ----------------------------------------------------------------------
# Exact Weyl Dimension Formulas
# ----------------------------------------------------------------------

def dim_so8(h):
    # D4: h = (h1, h2, h3, h4)
    l = [h[0] + 3, h[1] + 2, h[2] + 1, h[3]]
    num = 1
    for i in range(4):
        for j in range(i + 1, 4):
            num *= (l[i] - l[j]) * (l[i] + l[j])
    den = 1
    rho = [3, 2, 1, 0]
    for i in range(4):
        for j in range(i + 1, 4):
            den *= (rho[i] - rho[j]) * (rho[i] + rho[j])
    return int(round(abs(num) / den))

def dim_so9(h):
    # B4: h = (h1, h2, h3, h4)
    l = [h[0] + 3.5, h[1] + 2.5, h[2] + 1.5, h[3] + 0.5]
    num = 1
    for i in range(4):
        num *= l[i]
        for j in range(i + 1, 4):
            num *= (l[i] - l[j]) * (l[i] + l[j])
    den = 1
    rho = [3.5, 2.5, 1.5, 0.5]
    for i in range(4):
        den *= rho[i]
        for j in range(i + 1, 4):
            den *= (rho[i] - rho[j]) * (rho[i] + rho[j])
    return int(round(abs(num) / den))

def dim_so10(H):
    # D5: H = (H1, H2, H3, H4, H5)
    l = [H[0] + 4, H[1] + 3, H[2] + 2, H[3] + 1, H[4]]
    num = 1
    for i in range(5):
        for j in range(i + 1, 5):
            num *= (l[i] - l[j]) * (l[i] + l[j])
    den = 1
    rho = [4, 3, 2, 1, 0]
    for i in range(5):
        for j in range(i + 1, 5):
            den *= (rho[i] - rho[j]) * (rho[i] + rho[j])
    return int(round(abs(num) / den))

# ----------------------------------------------------------------------
# Exact Branching Rules
# ----------------------------------------------------------------------

def branch_so9_to_so8(h):
    """Branches an SO(9) irrep (h1, h2, h3, h4) into SO(8) irreps."""
    h1, h2, h3, h4 = h
    is_half = (abs(h1 - int(h1)) > 0.1)
    res = defaultdict(int)
    for g1 in [h2 + k for k in range(int(h1 - h2) + 1)]:
        for g2 in [h3 + k for k in range(int(h2 - h3) + 1)]:
            for g3 in [h4 + k for k in range(int(h3 - h4) + 1)]:
                if is_half:
                    val = 0.5
                    while val <= h4 + 1e-5:
                        res[(g1, g2, g3, val)] += 1
                        res[(g1, g2, g3, -val)] += 1
                        val += 1.0
                else:
                    h4_max = int(h4)
                    res[(g1, g2, g3, 0)] += 1
                    for v in range(1, h4_max + 1):
                        res[(g1, g2, g3, v)] += 1
                        res[(g1, g2, g3, -v)] += 1
    return dict(res)

def branch_so10_to_so9(H):
    """Branches an SO(10) irrep (H1, H2, H3, H4, H5) into SO(9) irreps."""
    H1, H2, H3, H4, H5 = H
    abs_H5 = abs(H5)
    res = defaultdict(int)
    for h1 in [H2 + k for k in range(int(H1 - H2) + 1)]:
        for h2 in [H3 + k for k in range(int(H2 - H3) + 1)]:
            for h3 in [H4 + k for k in range(int(H3 - H4) + 1)]:
                for h4 in [abs_H5 + k for k in range(int(H4 - abs_H5) + 1)]:
                    res[(h1, h2, h3, h4)] += 1
    return dict(res)

# ----------------------------------------------------------------------
# Tensor / Spinor Name Helper
# ----------------------------------------------------------------------

def format_weight(w):
    return "(" + ", ".join(f"{x:g}" for x in w) + ")"

def tensor_name_so8(w):
    is_f = abs(w[0] - int(w[0])) > 0.1
    if not is_f:
        if w == (0, 0, 0, 0): return "Scalar (1)"
        if w == (1, 0, 0, 0): return "Vector (8_v)"
        if w == (1, 1, 0, 0): return "2-form (28)"
        if w == (2, 0, 0, 0): return "Sym traceless rank 2 (35_v)"
        if w == (1, 1, 1, 1): return "Self-dual 4-form (35_s)"
        if w == (1, 1, 1, -1): return "Anti-self-dual 4-form (35_c)"
        if w == (1, 1, 1, 0): return "3-form (56_v)"
        if w == (2, 1, 0, 0): return "Young (2,1) mixed tensor (112)"
        if w == (3, 0, 0, 0): return "Sym traceless rank 3 (84)"
    else:
        if w == (0.5, 0.5, 0.5, 0.5): return "Chiral spinor (8_s)"
        if w == (0.5, 0.5, 0.5, -0.5): return "Anti-chiral spinor (8_c)"
        if w == (1.5, 0.5, 0.5, 0.5): return "Spin-3/2 vector-spinor (56_s)"
        if w == (1.5, 0.5, 0.5, -0.5): return "Spin-3/2 vector-spinor (56_c)"
    return ""

def tensor_name_so9(w):
    is_f = abs(w[0] - int(w[0])) > 0.1
    if not is_f:
        if w == (0, 0, 0, 0): return "Scalar (1)"
        if w == (1, 0, 0, 0): return "Vector (9)"
        if w == (1, 1, 0, 0): return "2-form (36)"
        if w == (2, 0, 0, 0): return "Sym traceless rank 2 (44)"
        if w == (1, 1, 1, 0): return "3-form (84)"
        if w == (1, 1, 1, 1): return "4-form (126)"
        if w == (3, 0, 0, 0): return "Sym traceless rank 3 (156)"
        if w == (2, 1, 0, 0): return "Young (2,1) mixed tensor (231)"
        if w == (2, 1, 1, 0): return "Young (2,1,1) mixed tensor (594)"
        if w == (4, 0, 0, 0): return "Sym traceless rank 4 (450)"
        if w == (3, 1, 0, 0): return "Young (3,1) mixed tensor (910)"
        if w == (5, 0, 0, 0): return "Sym traceless rank 5 (1122)"
    else:
        if w == (0.5, 0.5, 0.5, 0.5): return "Majorana spinor (16)"
        if w == (1.5, 0.5, 0.5, 0.5): return "Vector-spinor (128)"
        if w == (1.5, 1.5, 0.5, 0.5): return "2-form spinor (432)"
        if w == (2.5, 0.5, 0.5, 0.5): return "Sym rank 2 spinor (576)"
        if w == (3.5, 0.5, 0.5, 0.5): return "Sym rank 3 spinor (1920)"
    return ""

def tensor_name_so10(w):
    is_f = abs(w[0] - int(w[0])) > 0.1
    if not is_f:
        if w == (0, 0, 0, 0, 0): return "Scalar (1)"
        if w == (1, 0, 0, 0, 0): return "Vector (10)"
        if w == (1, 1, 0, 0, 0): return "2-form / Adjoint (45)"
        if w == (2, 0, 0, 0, 0): return "Sym traceless rank 2 (54)"
        if w == (1, 1, 1, 0, 0): return "3-form (120)"
        if w == (1, 1, 1, 1, 1): return "Chiral self-dual 5-form (126)"
        if w == (1, 1, 1, 1, -1): return "Anti-chiral 5-form (126*)"
        if w == (1, 1, 1, 1, 0): return "4-form (210)"
        if w == (3, 0, 0, 0, 0): return "Sym traceless rank 3 (210')"
        if w == (2, 1, 0, 0, 0): return "Young (2,1) mixed tensor (320)"
        if w == (2, 1, 1, 0, 0): return "Young (2,1,1) mixed tensor (945)"
        if w == (3, 1, 0, 0, 0): return "Young (3,1) mixed tensor (1386)"
        if w == (5, 0, 0, 0, 0): return "Sym traceless rank 5 (1782)"
    else:
        if w == (0.5, 0.5, 0.5, 0.5, 0.5): return "Weyl spinor (16)"
        if w == (0.5, 0.5, 0.5, 0.5, -0.5): return "Anti-Weyl spinor (16*)"
        if w == (1.5, 0.5, 0.5, 0.5, 0.5): return "Vector-spinor (144)"
        if w == (1.5, 1.5, 0.5, 0.5, 0.5): return "2-form spinor (560)"
        if w == (2.5, 0.5, 0.5, 0.5, 0.5): return "Sym rank 2 spinor (720)"
        if w == (3.5, 0.5, 0.5, 0.5, 0.5): return "Sym rank 3 spinor (2640)"
    return ""

# ----------------------------------------------------------------------
# Generation of Irreps up to Max Dimension
# ----------------------------------------------------------------------

def generate_so8_reps(max_dim=4000):
    reps = []
    # Bosons
    for h1 in range(8):
        for h2 in range(h1 + 1):
            for h3 in range(h2 + 1):
                for h4 in range(-h3, h3 + 1):
                    w = (h1, h2, h3, h4)
                    d = dim_so8(w)
                    if 0 < d <= max_dim:
                        reps.append((d, "B", w))
    # Fermions
    for i1 in range(7):
        for i2 in range(i1 + 1):
            for i3 in range(i2 + 1):
                for i4 in range(i3 + 1):
                    for sign in [1, -1] if i4 > 0 else [1, -1]:
                        w = (i1 + 0.5, i2 + 0.5, i3 + 0.5, (i4 + 0.5) * sign)
                        d = dim_so8(w)
                        if 0 < d <= max_dim:
                            reps.append((d, "F", w))
    reps = sorted(list(set(reps)), key=lambda x: (x[0], x[1], x[2]))
    return reps

def generate_so9_reps(max_dim=4000):
    reps = []
    # Bosons
    for h1 in range(8):
        for h2 in range(h1 + 1):
            for h3 in range(h2 + 1):
                for h4 in range(h3 + 1):
                    w = (h1, h2, h3, h4)
                    d = dim_so9(w)
                    if 0 < d <= max_dim:
                        reps.append((d, "B", w))
    # Fermions
    for i1 in range(7):
        for i2 in range(i1 + 1):
            for i3 in range(i2 + 1):
                for i4 in range(i3 + 1):
                    w = (i1 + 0.5, i2 + 0.5, i3 + 0.5, i4 + 0.5)
                    d = dim_so9(w)
                    if 0 < d <= max_dim:
                        reps.append((d, "F", w))
    reps = sorted(list(set(reps)), key=lambda x: (x[0], x[1], x[2]))
    return reps

def generate_so10_reps(max_dim=4000):
    reps = []
    # Bosons
    for H1 in range(7):
        for H2 in range(H1 + 1):
            for H3 in range(H2 + 1):
                for H4 in range(H3 + 1):
                    for H5 in range(-H4, H4 + 1):
                        w = (H1, H2, H3, H4, H5)
                        d = dim_so10(w)
                        if 0 < d <= max_dim:
                            reps.append((d, "B", w))
    # Fermions
    for i1 in range(6):
        for i2 in range(i1 + 1):
            for i3 in range(i2 + 1):
                for i4 in range(i3 + 1):
                    for i5 in range(i4 + 1):
                        for sign in [1, -1] if i5 > 0 else [1, -1]:
                            w = (i1 + 0.5, i2 + 0.5, i3 + 0.5, i4 + 0.5, (i5 + 0.5) * sign)
                            d = dim_so10(w)
                            if 0 < d <= max_dim:
                                reps.append((d, "F", w))
    reps = sorted(list(set(reps)), key=lambda x: (x[0], x[1], x[2]))
    return reps

# ----------------------------------------------------------------------
# Pretty Printer Functions
# ----------------------------------------------------------------------

def print_so_reps_table(title, reps, name_fn):
    print("=" * 90)
    print(f"{title}")
    print("=" * 90)
    print(f"{'Dim':<8} {'Type':<6} {'Highest Weight Vector':<28} {'Description'}")
    print("-" * 90)
    for d, t, w in reps:
        tname = name_fn(w)
        print(f"{d:<8} {t:<6} {format_weight(w):<28} {tname}")
    print()

def print_branching_so10_to_so9(reps_so10):
    print("=" * 90)
    print("SO(10) -> SO(9) BRANCHING RULES (FOR SO(10) REPS UP TO DIM 4000)")
    print("=" * 90)
    print(f"{'SO(10) Rep':<32} -> {'SO(9) Branching Decomposition'}")
    print("-" * 90)
    for d, t, w in reps_so10:
        b = branch_so10_to_so9(w)
        # Sort branches by dimension descending
        sorted_branches = sorted(b.items(), key=lambda x: -dim_so9(x[0]))
        branch_str = " + ".join(
            (f"{m}*" if m > 1 else "") + f"{dim_so9(h)}_{format_weight(h)}"
            for h, m in sorted_branches
        )
        so10_str = f"{d}_{format_weight(w)}"
        print(f"{so10_str:<32} -> {branch_str}")
    print()

def print_branching_so9_to_so8(reps_so9):
    print("=" * 90)
    print("SO(9) -> SO(8) BRANCHING RULES (FOR SO(9) REPS UP TO DIM 4000)")
    print("=" * 90)
    print(f"{'SO(9) Rep':<30} -> {'SO(8) Branching Decomposition'}")
    print("-" * 90)
    for d, t, w in reps_so9:
        b = branch_so9_to_so8(w)
        sorted_branches = sorted(b.items(), key=lambda x: -dim_so8(x[0]))
        branch_str = " + ".join(
            (f"{m}*" if m > 1 else "") + f"{dim_so8(h)}_{format_weight(h)}"
            for h, m in sorted_branches
        )
        so9_str = f"{d}_{format_weight(w)}"
        print(f"{so9_str:<30} -> {branch_str}")
    print()

if __name__ == "__main__":
    import sys
    max_d = 4000
    if len(sys.argv) > 1:
        max_d = int(sys.argv[1])
        
    so8_reps = generate_so8_reps(max_d)
    so9_reps = generate_so9_reps(max_d)
    so10_reps = generate_so10_reps(max_d)
    
    print_so_reps_table("1. SO(8) REPRESENTATIONS (DIM <= 4000)", so8_reps, tensor_name_so8)
    print_so_reps_table("2. SO(9) REPRESENTATIONS (DIM <= 4000)", so9_reps, tensor_name_so9)
    print_so_reps_table("3. SO(10) REPRESENTATIONS (DIM <= 4000)", so10_reps, tensor_name_so10)
    
    print_branching_so10_to_so9(so10_reps)
    print_branching_so9_to_so8(so9_reps)
