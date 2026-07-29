# F5 Scientific Calculator — `f(x) = a · bˣ`

A from-scratch scientific calculator for the transcendental function
**F5: `f(x) = a · bˣ`** (with `b > 0`), built for SOEN 6011 (Software
Engineering Processes), Concordia University.

The numerical core computes `a · bˣ = a · exp(x · ln b)` using **range-reduced
series expansions for `ln` and `exp`** — no `math` library, no `**` operator,
and no built-in numeric helpers. It ships with a **Tkinter** graphical
interface and a **PyUnit** test suite.

---

## Function

| Symbol | Meaning              | Domain                    |
| ------ | -------------------- | ------------------------- |
| `a`    | coefficient          | any real number           |
| `b`    | base / growth factor | **`b > 0`** (required)    |
| `x`    | exponent / variable  | any real number           |

`b > 1` models growth, `0 < b < 1` models decay, and negative `x` is supported.

---

## Requirements

- Python 3.8 or newer (standard library only)
- Tkinter — bundled with most Python installations
  (on Debian/Ubuntu: `sudo apt install python3-tk`)

No third-party packages, IDE, or build tool is required.

---

## Running

```bash
# Graphical interface
python3 src/f5_gui.py

# Test suite (PyUnit)
python3 -m unittest discover -s src -p "test_*.py" -v
```

---

## Project layout

```
src/
  f5_gui.py         Tkinter graphical user interface (entry point)
  f5_mathcore.py    From-scratch numerical core (ln, exp, and helpers)
  f5_exceptions.py  Custom exception hierarchy
  test_f5_d2.py     PyUnit test suite
output/
  gui.png           The interface computing 3 · 2⁴ = 48
```

---

## Design notes

**From scratch.** Only input, output, arithmetic, and user-interface
functions are used. The transcendental math (`ln`, `exp`) and the numeric
helpers `abs`, `round`, `floor`, and `2ⁿ` are all re-implemented by hand in
`f5_mathcore.py`.

**Accuracy.** Worst-case relative error versus a reference over 50,000
randomized inputs is approximately `7.5e-14` (about 13 significant decimal
digits).

**Error handling.** A small exception hierarchy
(`CalculatorError → DomainError, OverflowGuard, InputError`) surfaces
plain-language messages: a non-positive base, an out-of-range result, or an
unparseable / empty field each produce a specific, actionable message.

---

## Author

Aafreen Fathima — Student ID 40331369
SOEN 6011 (Section CC), Summer 2026 — Concordia University
