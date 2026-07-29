#!/usr/bin/env python3
"""
SOEN 6011 - Summer 2026 - Deliverable 2, Problem 5
Function F5:  f(x) = a * b^x    [a, b real constants; x real variable; b > 0]

NUMERICAL CORE - implemented FROM SCRATCH.

"From scratch" (per the project): apart from input, output, arithmetic, and
user-interface functions, the implementation uses NO built-in or library
functions provided by Python. In particular this module uses no `math`
library, no `**` power operator, and no built-in numeric helpers such as
abs(), round(), int(), or pow(). Every non-arithmetic operation below is
implemented by a subordinate function.

Strategy (selected in D1, Problem 4 - Algorithm 1):

        a * b^x = a * exp( x * ln(b) )

with ln and exp evaluated by range-reduced series expansions.
"""

from f5_exceptions import DomainError, OverflowGuard

# --- Constants (literals are data, not function calls) --------------------
LN2 = 0.6931471805599453          # ln(2)
EPS = 1e-17                       # series convergence threshold
MAX_T = 709.782712893384          # ln(largest finite double) -> overflow above
MIN_T = -745.133219101941         # exp underflows to 0 below this
MAX_ITER = 1000                   # convergence-loop safety cap


# ==========================================================================
# Arithmetic primitives implemented from scratch
# (replacing the built-ins abs, round-to-int, and the ** operator)
# ==========================================================================
def _abs(v):
    """Absolute value without built-in abs()."""
    if v < 0.0:
        return -v
    return v


def _floor_to_int(v):
    """
    Largest integer <= v, returned as a Python int, without int()/floor().
    Uses only comparison and integer arithmetic on an accumulator.
    """
    n = 0
    if v >= 0.0:
        while n + 1 <= v:
            n = n + 1
        return n
    # negative: go downward until n <= v
    while n > v:
        n = n - 1
    return n


def _round_to_int(v):
    """Nearest integer to v (round-half-up) without round()."""
    return _floor_to_int(v + 0.5)


def _int_pow2(n):
    """
    Compute 2**n for integer n, without the ** operator, by repeated
    multiplication (exponentiation by squaring on base 2).
    Handles negative n by reciprocal.
    """
    negative = n < 0
    if negative:
        n = -n
    result = 1.0
    base = 2.0
    while n > 0:
        if n - (n // 2) * 2 == 1:      # n is odd  (n mod 2 == 1)
            result = result * base
        base = base * base
        n = n // 2                     # integer floor division: arithmetic
    if negative:
        return 1.0 / result
    return result


# ==========================================================================
# Subordinate transcendental functions (Problem 3, Algorithm 1)
# ==========================================================================
def _ln(b):
    """Natural logarithm via range reduction + atanh series (requires b > 0)."""
    if b <= 0.0:
        raise DomainError(
            "Cannot take the logarithm of b = {0}. The base b must be "
            "greater than 0.".format(b)
        )
    # Range reduce: b = m * 2**e  with m in [1, 2), using only *, / by 2.
    e = 0
    m = b
    while m >= 2.0:
        m = m * 0.5
        e = e + 1
    while m < 1.0:
        m = m * 2.0
        e = e - 1
    # atanh series: ln(m) = 2 * sum y^(2k+1)/(2k+1),  y = (m-1)/(m+1)
    y = (m - 1.0) / (m + 1.0)
    y2 = y * y
    term = y
    total = 0.0
    k = 0
    count = 0
    while count < MAX_ITER:
        delta = term / (2 * k + 1)
        total = total + delta
        if _abs(delta) < EPS:
            break
        term = term * y2
        k = k + 1
        count = count + 1
    return 2.0 * total + e * LN2


def _exp(t):
    """e**t via range reduction + Taylor series (from scratch)."""
    if t > MAX_T:
        raise OverflowGuard(
            "The exponent is too large: b^x would exceed the largest number "
            "this calculator can represent. Try a smaller x or a base closer "
            "to 1."
        )
    if t < MIN_T:
        return 0.0                        # graceful underflow
    # Range reduce: t = n*ln2 + r, |r| <= ln2/2
    n = _round_to_int(t / LN2)
    r = t - n * LN2
    # Taylor: e**r = sum r**k / k!
    term = 1.0
    total = 1.0
    k = 1
    count = 0
    while count < MAX_ITER:
        term = term * r / k
        total = total + term
        if _abs(term) < EPS:
            break
        k = k + 1
        count = count + 1
    return total * _int_pow2(n)           # 2**n from scratch


# ==========================================================================
# Public function
# ==========================================================================
def power_abx(a, b, x):
    """
    Compute a * b**x from scratch.

    Raises:
        DomainError    - if b <= 0 (result would not be real).
        OverflowGuard  - if the magnitude exceeds the representable range.
    """
    if b <= 0.0:
        raise DomainError(
            "The base b must be greater than 0 (you entered b = {0}). "
            "A non-positive base raised to a fractional power is not a real "
            "number.".format(b)
        )
    if a == 0.0:
        return 0.0                        # 0 * anything finite is 0
    if b == 1.0:
        return a                          # 1**x == 1, so result is a
    t = x * _ln(b)                        # exponent of the exp-log identity
    m = _exp(t)                           # b**x
    result = a * m
    # Overflow can also strike in the final multiply by a. Detect an infinite
    # result by comparing against +/- infinity, obtained from arithmetic
    # overflow of a large literal (no math library used).
    inf = 1e308 * 10.0                              # overflows to +inf
    if result == inf or result == -inf:
        raise OverflowGuard(
            "The result is too large for this calculator to represent "
            "(a * b^x overflowed). Try smaller magnitudes."
        )
    return result
