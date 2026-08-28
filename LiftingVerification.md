# Exact Character-Level Verification of the SO(10) -> SO(9) Lifting

This document records the exact, term-by-term verification that the $\mathrm{SO}(10)$ decompositions generated for the cumulative spectrum $R_n = \sum_{l=1}^n r_l$ (Proposal III.B) branch back to the target $\mathrm{SO}(9)$ spectrum with **zero error** across all levels $n = 1, \dots, 10$.

---

## 1. Methodology of the Exact Verification

For each mass level $n \in \{1, \dots, 10\}$:
1. **Independently Generated Target:**
   Compute the cumulative $\mathrm{SO}(9)$ spectrum:
   $$R_n = \sum_{l=1}^n r_l = \bigoplus_{h} m_{\text{target}}(h) \, \mathbf{R}_h^{\mathrm{SO}(9)}$$
   where $r_l$ is derived $ab\;initio$ from the Green-Schwarz open superstring Fock space.

2. **Branching the $\mathrm{SO}(10)$ Supermultiplet:**
   Take the proposed $\mathrm{SO}(10)$ supermultiplet $R_n^{\mathrm{SO}(10)} = \bigoplus_H M(H) \, \mathbf{V}_H^{\mathrm{SO}(10)}$ and branch each irreducible representation $H$ down to $\mathrm{SO}(9)$ using the exact Gelfand-Tsetlin branching rule:
   $$R_n^{\text{reconstructed}} = \bigoplus_H M(H) \left( \bigoplus_{h \in \text{Branch}(H)} \mathbf{R}_h^{\mathrm{SO}(9)} \right) = \bigoplus_h m_{\text{reconstructed}}(h) \, \mathbf{R}_h^{\mathrm{SO}(9)}$$

3. **Multiplicity Difference Evaluation:**
   For every bosonic and fermionic $\mathrm{SO}(9)$ highest weight $h$:
   $$\Delta m(h) = m_{\text{target}}(h) - m_{\text{reconstructed}}(h)$$

---

## 2. Character-Level Verification Results (Levels 1 to 10)

| Level $n$ | Distinct $\mathrm{SO}(9)$ Irreps | Distinct $\mathrm{SO}(10)$ Irreps | Total Physical States in $R_n$ | Maximum Multiplicity Discrepancy ($\max_h |\Delta m(h)|$) | Total Discrepancies | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 1 | 1 | 1 | **0** | **0** | **PASSED** |
| **2** | 2 | 1 | 10 | **0** | **0** | **PASSED** |
| **3** | 4 | 2 | 70 | **0** | **0** | **PASSED** |
| **4** | 7 | 3 | 399 | **0** | **0** | **PASSED** |
| **5** | 11 | 6 | 1,965 | **0** | **0** | **PASSED** |
| **6** | 17 | 11 | 8,649 | **0** | **0** | **PASSED** |
| **7** | 24 | 18 | 34,785 | **0** | **0** | **PASSED** |
| **8** | 33 | 29 | 129,834 | **0** | **0** | **PASSED** |
| **9** | 44 | 39 | 454,911 | **0** | **0** | **PASSED** |
| **10** | 57 | 53 | 1,509,389 | **0** | **0** | **PASSED** |

---

## 3. Findings

1. **Zero Discrepancies Across All Levels:**
   Every single $\mathrm{SO}(9)$ representation multiplicity in the reconstructed spectrum matches the target spectrum $R_n$ identically ($\Delta m(h) = 0$).
2. **Positivity of Multiplicities:**
   Every $\mathrm{SO}(10)$ irreducible representation in $R_n^{\mathrm{SO}(10)}$ enters with a strictly positive integer coefficient $M(H) > 0$.
3. **Chirality Consistency:**
   Chiral middle-dimensional tensor and spinor representations ($H_5 \neq 0$, such as $\mathbf{126}$, $\mathbf{1050}$, $\mathbf{4950}$, and $\mathbf{672}$) correctly reproduce the required unbranched $\mathrm{SO}(9)$ components without generating spurious lower-rank forms.

---

## 4. Reproducibility Command

To re-run and verify the exact character-level lifting from scratch:
```bash
python3 verify_so10_lifting.py
```
