# Mathematical Uniqueness and Exact Verification of the Supersymmetry Factorization

This document explains why the quotient polynomial $Q_n(x)$ in the character factorization $\mathcal{F}_n(x) = Q_n(x) \cdot \chi_{\text{susy}}(x)$ is mathematically unique, and records the empirical verification that $Q_n(x) \times (\mathbf{8}_v + \mathbf{8}_s) \equiv \mathcal{F}_n(x)$ across all levels $n = 1, \dots, 10$.

---

## 1. Uniqueness of the Quotient Polynomial

The representation characters of $\mathrm{SO}(8)$ live in the Laurent polynomial ring:
$$\mathcal{R} = \mathbb{Z}[x_1^{\pm 1}, x_2^{\pm 1}, x_3^{\pm 1}, x_4^{\pm 1}]$$

Because $\mathbb{Z}$ is an integral domain, the Laurent polynomial ring $\mathcal{R}$ is also an **integral domain** (it contains no non-zero zero-divisors).

### The Uniqueness Argument:
1. Suppose there exist two quotient polynomials $Q_n(x)$ and $Q'_n(x)$ satisfying:
   $$\mathcal{F}_n(x) = Q_n(x) \, \chi_{\text{susy}}(x) = Q'_n(x) \, \chi_{\text{susy}}(x)$$
2. Subtracting the two expressions gives:
   $$(Q_n(x) - Q'_n(x)) \, \chi_{\text{susy}}(x) = 0$$
3. Since $\chi_{\text{susy}}(x) \neq 0$ and $\mathcal{R}$ is an integral domain:
   $$Q_n(x) - Q'_n(x) = 0 \implies Q_n(x) = Q'_n(x)$$

Thus, the factorization quotient $Q_n(x)$, if it exists, is **strictly unique**.

### Determinism of Greedy Division:
Under any fixed monomial ordering (such as lexicographic order on weight vectors), the divisor:
$$\chi_{\text{susy}}(x) = \sum_{w \in \mathbf{8}_v} e^{w \cdot x} + \sum_{w \in \mathbf{8}_s} e^{w \cdot x}$$
has a unique leading term with coefficient $1$ (namely $e^{(1,0,0,0) \cdot x}$). 

Because the leading coefficient is $1$, standard leading-term polynomial division:
$$\mathcal{F}_n(x) = Q_n(x) \, \chi_{\text{susy}}(x) + R_n(x)$$
is strictly deterministic. Once the algorithm terminates with remainder $R_n(x) \equiv 0$, the resulting $Q_n(x)$ is guaranteed to be the exact and unique quotient.

---

## 2. Numerical Verification: Reconstructing $\mathcal{F}_n$ from $Q_n \times (\mathbf{8}_v + \mathbf{8}_s)$

To confirm this independently, the script [`verify_factorization.py`](verify_factorization.py) computes the explicit polynomial product:
$$\mathcal{F}_n^{\text{reconstructed}}(x) = Q_n(x) \times \left( \sum_{w \in \mathbf{8}_v} e^{w \cdot x} + \sum_{w \in \mathbf{8}_s} e^{w \cdot x} \right)$$
and compares $\mathcal{F}_n^{\text{reconstructed}}(x)$ term-by-term against the raw Green-Schwarz Fock space character $\mathcal{F}_n(x)$ for every single weight.

### Results Across Levels 1 to 10

| Level $n$ | Total Monomials in $\mathcal{F}_n$ | Total Monomials in $Q_n$ | Exact Term-by-Term Match | Maximum Discrepancy ($\max \|c_{\text{orig}} - c_{\text{recon}}\|$) | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 16 | 1 | $\mathcal{F}_1 \equiv Q_1 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **2** | 89 | 9 | $\mathcal{F}_2 \equiv Q_2 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **3** | 297 | 57 | $\mathcal{F}_3 \equiv Q_3 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **4** | 753 | 209 | $\mathcal{F}_4 \equiv Q_4 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **5** | 1,601 | 561 | $\mathcal{F}_5 \equiv Q_5 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **6** | 3,017 | 1,241 | $\mathcal{F}_6 \equiv Q_6 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **7** | 5,209 | 2,409 | $\mathcal{F}_7 \equiv Q_7 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **8** | 8,417 | 4,257 | $\mathcal{F}_8 \equiv Q_8 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **9** | 12,913 | 7,009 | $\mathcal{F}_9 \equiv Q_9 \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |
| **10** | 19,001 | 10,921 | $\mathcal{F}_{10} \equiv Q_{10} \times (\mathbf{8}_v + \mathbf{8}_s)$ | **0** | **PASSED** |

---

## 3. How to Reproduce

Run the dedicated factorization verifier:
```bash
python3 verify_factorization.py
```
This executes the forward division and the backward polynomial multiplication, verifying that every single coefficient and weight matches with zero error.
