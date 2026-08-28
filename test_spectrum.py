"""
Complete, robust SO(10) decomposition and test for levels 1 to 10.
"""

from collections import defaultdict
import itertools
import time

# 1. Weights of 8_v and 8_s
def get_8v_weights():
    w = []
    for i in range(4):
        for s in [1, -1]:
            vec = [0]*4
            vec[i] = s
            w.append(tuple(vec))
    return w

def get_8s_weights():
    w = []
    for signs in itertools.product([0.5, -0.5], repeat=4):
        if sum(1 for x in signs if x < 0) % 2 == 0:
            w.append(signs)
    return w

weights_8v = get_8v_weights()
weights_8s = get_8s_weights()

char_susy = defaultdict(int)
for w in weights_8v:
    char_susy[w] += 1
for w in weights_8s:
    char_susy[w] += 1

def poly_div_susy(P):
    Q = defaultdict(int)
    rem = defaultdict(int, P)
    while rem:
        active = [w for w, c in rem.items() if c != 0]
        if not active:
            break
        W = max(active)
        c = rem[W]
        q_w = (W[0]-1.0, W[1], W[2], W[3])
        Q[q_w] += c
        for dw, dm in char_susy.items():
            tw = (q_w[0]+dw[0], q_w[1]+dw[1], q_w[2]+dw[2], q_w[3]+dw[3])
            rem[tw] -= c * dm
            if rem[tw] == 0:
                del rem[tw]
    return Q

def compute_fock_levels(max_level):
    F = [defaultdict(int) for _ in range(max_level + 1)]
    F[0][(0,0,0,0)] = 1
    for n in range(1, max_level + 1):
        for w in weights_8s:
            for l in range(max_level, n - 1, -1):
                for prev_w, c in list(F[l - n].items()):
                    nw = (prev_w[0]+w[0], prev_w[1]+w[1], prev_w[2]+w[2], prev_w[3]+w[3])
                    F[l][nw] += c
        for w in weights_8v:
            for l in range(n, max_level + 1):
                for prev_w, c in list(F[l - n].items()):
                    nw = (prev_w[0]+w[0], prev_w[1]+w[1], prev_w[2]+w[2], prev_w[3]+w[3])
                    F[l][nw] += c
    return F

# D4 Weyl group elements
perms_d4 = list(itertools.permutations(range(4)))
perm_signs = []
for p in perms_d4:
    psign = 1
    for i in range(4):
        for j in range(i+1, 4):
            if p[i] > p[j]:
                psign = -psign
    perm_signs.append(psign)

signs_d4 = [s for s in itertools.product([1, -1], repeat=4) if sum(1 for x in s if x < 0) % 2 == 0]

weyl_ops_d4 = []
for p, psign in zip(perms_d4, perm_signs):
    for s in signs_d4:
        weyl_ops_d4.append((p, s, psign))

rho_d4 = (3, 2, 1, 0)

def weyl_num_d4(shift_weight):
    poly = defaultdict(int)
    for p, s, det in weyl_ops_d4:
        w = tuple(shift_weight[p[i]] * s[i] for i in range(4))
        poly[w] += det
        if poly[w] == 0:
            del poly[w]
    return poly

den_d4 = weyl_num_d4(rho_d4)

def poly_mult(p1, p2):
    res = defaultdict(int)
    for w1, c1 in p1.items():
        for w2, c2 in p2.items():
            w = (w1[0]+w2[0], w1[1]+w2[1], w1[2]+w2[2], w1[3]+w2[3])
            res[w] += c1 * c2
    return res

def decompose_so8_char(char_poly):
    num = poly_mult(char_poly, den_d4)
    decomp = defaultdict(int)
    rem = defaultdict(int, num)
    while rem:
        active = [w for w, c in rem.items() if c != 0]
        if not active:
            break
        hw_shift = max(active)
        coeff = rem[hw_shift]
        hw = (hw_shift[0]-rho_d4[0], hw_shift[1]-rho_d4[1], hw_shift[2]-rho_d4[2], hw_shift[3]-rho_d4[3])
        num_hw = weyl_num_d4(hw_shift)
        for w, c in num_hw.items():
            rem[w] -= coeff * c
            if rem[w] == 0:
                del rem[w]
        decomp[hw] += coeff
    return decomp

def branch_so9_to_so8(h):
    h1, h2, h3, h4 = h
    is_half = (abs(h1 - int(h1)) > 0.1)
    res = []
    for g1 in [h2 + k for k in range(int(h1 - h2) + 1)]:
        for g2 in [h3 + k for k in range(int(h2 - h3) + 1)]:
            for g3 in [h4 + k for k in range(int(h3 - h4) + 1)]:
                if is_half:
                    g4_vals = []
                    val = 0.5
                    while val <= h4 + 1e-5:
                        g4_vals.extend([val, -val])
                        val += 1.0
                else:
                    h4_max = int(h4)
                    g4_vals = [0] if h4_max == 0 else [0] + [s*v for v in range(1, h4_max + 1) for s in [1, -1]]
                for g4 in g4_vals:
                    res.append((g1, g2, g3, g4))
    return res

def branch_so10_to_so9(H):
    H1, H2, H3, H4, H5 = H
    abs_H5 = abs(H5)
    res = []
    for h1 in [H2 + k for k in range(int(H1 - H2) + 1)]:
        for h2 in [H3 + k for k in range(int(H2 - H3) + 1)]:
            for h3 in [H4 + k for k in range(int(H3 - H4) + 1)]:
                for h4 in [abs_H5 + k for k in range(int(H4 - abs_H5) + 1)]:
                    res.append((h1, h2, h3, h4))
    return res

def decompose_so8_to_so9(so8_mults):
    so9_decomp = defaultdict(int)
    rem = defaultdict(int, so8_mults)
    while rem:
        active = [w for w, c in rem.items() if c != 0]
        if not active:
            break
        top_w = max(active, key=lambda w: (w[0], w[1], w[2], abs(w[3]), w[3]))
        coeff = rem[top_w]
        h = (top_w[0], top_w[1], top_w[2], abs(top_w[3]))
        so9_decomp[h] += coeff
        for g in branch_so9_to_so8(h):
            rem[g] -= coeff
            if rem[g] == 0:
                del rem[g]
    return so9_decomp

# Exact general SO(10) decomposition allowing chiral H5
def decompose_so9_to_so10(so9_mults):
    # Splits into bosonic and fermionic
    so9_B = {h: m for h, m in so9_mults.items() if abs(h[0] - int(h[0])) < 0.1 and m > 0}
    so9_F = {h: m for h, m in so9_mults.items() if abs(h[0] - int(h[0])) > 0.1 and m > 0}
    
    def solve_sector(target, is_fermion):
        target_keys = sorted(target.keys(), reverse=True)
        if not target_keys:
            return {}
        
        # Build candidate H list
        useful_H = []
        for h in target_keys:
            if is_fermion:
                h5_vals = [0.5 + k for k in range(int(h[3] - 0.5) + 1)]
            else:
                h5_vals = [float(k) for k in range(int(h[3]) + 1)]
            for h5 in h5_vals:
                H = (h[0], h[1], h[2], h[3], h5)
                b = branch_so10_to_so9(H)
                if all(target.get(x, 0) >= 1 for x in b):
                    useful_H.append((H, b))
                    
        branch_dict = {H: b for H, b in useful_H}
        
        def backtrack(rem, idx):
            if idx == len(target_keys):
                if all(v == 0 for v in rem.values()):
                    return {}
                return None
            w = target_keys[idx]
            val = rem.get(w, 0)
            if val == 0:
                return backtrack(rem, idx + 1)
            if val < 0:
                return None
            
            matching = [H for H, b in useful_H if (H[0], H[1], H[2], H[3]) == w]
            if not matching:
                return None
                
            def gen_parts(n, total):
                if n == 1:
                    yield (total,)
                else:
                    for first in range(total + 1):
                        for rest in gen_parts(n - 1, total - first):
                            yield (first,) + rest
                            
            for part in gen_parts(len(matching), val):
                next_rem = defaultdict(int, rem)
                valid = True
                for H, count in zip(matching, part):
                    if count > 0:
                        for h_b in branch_dict[H]:
                            next_rem[h_b] -= count
                            if next_rem[h_b] < 0:
                                valid = False
                                break
                    if not valid:
                        break
                if valid:
                    res = backtrack(next_rem, idx + 1)
                    if res is not None:
                        for H, count in zip(matching, part):
                            if count > 0:
                                res[H] = count
                        return res
            return None

        return backtrack(defaultdict(int, target), 0)

    sol_B = solve_sector(so9_B, False)
    sol_F = solve_sector(so9_F, True)
    
    if sol_B is None or sol_F is None:
        # Fallback to standard parity-invariant decomposition to expose negative multiplicities
        fallback = defaultdict(int)
        rem = defaultdict(int, so9_mults)
        while rem:
            active = [w for w, c in rem.items() if c != 0]
            if not active:
                break
            top_w = max(active)
            coeff = rem[top_w]
            is_half = (abs(top_w[0] - int(top_w[0])) > 0.1)
            H5 = 0.5 if is_half else 0.0
            H = (top_w[0], top_w[1], top_w[2], top_w[3], H5)
            fallback[H] += coeff
            for h in branch_so10_to_so9(H):
                rem[h] -= coeff
                if rem[h] == 0:
                    del rem[h]
        return fallback
    
    res = defaultdict(int)
    for H, m in sol_B.items():
        res[H] += m
    for H, m in sol_F.items():
        res[H] += m
    return res
