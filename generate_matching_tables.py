"""
Generate Markdown matching tables for Levels 1 to 10.
"""

from collections import defaultdict
from test_spectrum import (
    compute_fock_levels, poly_div_susy, decompose_so8_char,
    decompose_so8_to_so9, decompose_so9_to_so10
)
from generate_reference_tables import (
    dim_so9, dim_so10, tensor_name_so9, tensor_name_so10,
    format_weight, branch_so10_to_so9
)

def generate_markdown_tables(max_level=10):
    print(f"Computing string spectrum up to Level {max_level}...")
    F = compute_fock_levels(max_level)
    
    r_so9_list = [None]
    for l in range(1, max_level + 1):
        Q = poly_div_susy(F[l])
        so8_m = decompose_so8_char(Q)
        so9_m = decompose_so8_to_so9(so8_m)
        r_so9_list.append(so9_m)
        
    md_content = []
    md_content.append("# Term-by-Term Matching Tables: SO(9) Cumulative String Spectrum vs SO(10) Lift\n")
    md_content.append("This document contains the exact term-by-term verification tables for **Proposal III.B** across Levels 1 to 10.\n")
    md_content.append("For each level $n$, we compare:")
    md_content.append("1. The **Target Cumulative Spectrum**: $R^{(n)} = \\sum_{l=1}^n r^{(l)}$ (in $\\mathrm{SO}(9)$)")
    md_content.append("2. The **Reconstructed Spectrum**: obtained by branching the proposed $\\mathrm{SO}(10)$ supermultiplet down to $\\mathrm{SO}(9)$.\n")
    md_content.append("---\n")
    
    for n in range(1, max_level + 1):
        so9_cum = defaultdict(int)
        for l in range(1, n + 1):
            for h, m in r_so9_list[l].items():
                so9_cum[h] += m
                
        so10_decomp = decompose_so9_to_so10(so9_cum)
        
        so9_recon = defaultdict(int)
        for H, m in so10_decomp.items():
            for h, mb in branch_so10_to_so9(H).items():
                so9_recon[h] += m * mb
                
        md_content.append(f"## Level $n = {n}$\n")
        
        # SO(10) irreps summary
        so10_bosons = {H: m for H, m in so10_decomp.items() if abs(H[0] - int(H[0])) < 0.1}
        so10_fermions = {H: m for H, m in so10_decomp.items() if abs(H[0] - int(H[0])) > 0.1}
        
        md_content.append("### $\\mathrm{SO}(10)$ Supermultiplet Content")
        md_content.append("**Bosons:**")
        b_str = ", ".join(f"${m} \\times \\mathbf{{{dim_so10(H)}}}$ `{format_weight(H)}`" for H, m in sorted(so10_bosons.items(), key=lambda x: -dim_so10(x[0])))
        md_content.append(b_str + "\n")
        
        md_content.append("**Fermions:**")
        f_str = ", ".join(f"${m} \\times \\mathbf{{{dim_so10(H)}}}$ `{format_weight(H)}`" for H, m in sorted(so10_fermions.items(), key=lambda x: -dim_so10(x[0])))
        md_content.append(f_str + "\n")
        
        # Matching Table
        md_content.append("### $\\mathrm{SO}(9)$ Matching Verification Table")
        md_content.append("| Type | $\\mathrm{SO}(9)$ Highest Weight | $\\mathrm{SO}(9)$ Dim | Target Multiplicity (String) | Reconstructed Multiplicity (from $\\mathrm{SO}(10)$) | Difference | Status |")
        md_content.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        
        all_h = sorted(set(list(so9_cum.keys()) + list(so9_recon.keys())), key=lambda x: (abs(x[0] - int(x[0])) > 0.1, -dim_so9(x)))
        all_match = True
        for h in all_h:
            t_type = "F" if abs(h[0] - int(h[0])) > 0.1 else "B"
            m_target = so9_cum.get(h, 0)
            m_recon = so9_recon.get(h, 0)
            diff = m_target - m_recon
            if diff != 0: all_match = False
            status = "MATCH" if diff == 0 else f"**MISMATCH ({diff:+d})**"
            md_content.append(f"| {t_type} | `{format_weight(h)}` | **{dim_so9(h)}** | {m_target} | {m_recon} | {diff} | {status} |")
            
        md_content.append(f"\n**Level {n} Result:** {' PASSED (100% Exact Match)' if all_match else '❌ FAILED'}\n")
        md_content.append("---\n")
        
    with open("matching_tables.md", "w") as f:
        f.write("\n".join(md_content))
    print("matching_tables.md successfully created.")

if __name__ == "__main__":
    generate_markdown_tables(10)
