#!/usr/bin/env python3
"""
SOEN 6011 - Summer 2026 - Deliverable 2, Problem 5
Graphical user interface (Tkinter) for Function F5:  f(x) = a * b^x.

Run:  python3 f5_gui.py       (no IDE or build tool required)

The GUI depends only on the standard-library Tkinter toolkit (permitted as a
user-interface function) and on the project's own modules f5_mathcore and
f5_exceptions. All numerical work is performed by the from-scratch core.
"""

import tkinter as tk
from tkinter import ttk

from f5_mathcore import power_abx
from f5_exceptions import DomainError, OverflowGuard, InputError

TEAL = "#23373B"
ACCENT = "#C0651A"
BG = "#FAFAFA"
OKC = "#1E6B1E"
ERRC = "#B00020"

# Cross-platform monospace family: Tk picks the first that exists.
MONO = "Menlo"      # macOS; Tk falls back to Courier if absent


def _parse(field, raw):
    """Convert a text entry to float, raising InputError with the field name."""
    raw = raw.strip()
    try:
        return float(raw)                 # float() is an input/conversion func
    except ValueError:
        raise InputError(field, raw)


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("F5 Scientific Calculator   f(x) = a · b^x")
        root.configure(bg=BG)
        root.minsize(440, 340)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", background=BG, foreground=TEAL, font=("Helvetica", 11))
        style.configure("Head.TLabel", font=("Helvetica", 15, "bold"), foreground=TEAL)
        style.configure("Sub.TLabel", font=("Helvetica", 9), foreground="#5A6668")
        style.configure("TEntry", padding=4)
        style.configure("Go.TButton", font=("Helvetica", 11, "bold"),
                        foreground="white", background=ACCENT, padding=6)
        style.map("Go.TButton", background=[("active", "#9C5010")])

        pad = {"padx": 12, "pady": 6}

        ttk.Label(root, text="f(x) = a · b\u02e3", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", **pad)
        ttk.Label(root, text="Computes a times b to the power x, from scratch (b > 0).",
                  style="Sub.TLabel").grid(row=1, column=0, columnspan=2, sticky="w",
                                           padx=12)

        self.entries = {}
        for i, (key, label) in enumerate([
            ("a", "a  (coefficient)"),
            ("b", "b  (base, > 0)"),
            ("x", "x  (exponent)"),
        ]):
            ttk.Label(root, text=label).grid(row=2 + i, column=0, sticky="w", **pad)
            e = ttk.Entry(root, width=22, font=(MONO, 11))
            e.grid(row=2 + i, column=1, sticky="ew", **pad)
            e.bind("<Return>", lambda _evt: self.compute())
            self.entries[key] = e
        self.entries["a"].focus_set()

        btns = tk.Frame(root, bg=BG)
        btns.grid(row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=(4, 2))
        ttk.Button(btns, text="Compute", style="Go.TButton",
                   command=self.compute).pack(side="left")
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=8)

        self.result = tk.Text(root, height=4, width=48, wrap="word",
                              font=(MONO, 11), bg="white", fg=TEAL,
                              relief="solid", borderwidth=1, state="disabled")
        self.result.grid(row=6, column=0, columnspan=2, sticky="nsew",
                         padx=12, pady=(6, 12))

        root.columnconfigure(1, weight=1)
        root.rowconfigure(6, weight=1)

    # ------------------------------------------------------------------
    def _show(self, text, color=TEAL):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.configure(state="disabled", fg=color)

    def clear(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self._show("")
        self.entries["a"].focus_set()

    def compute(self):
        # 1) parse inputs (InputError names the offending field)
        try:
            a = _parse("a", self.entries["a"].get())
            b = _parse("b", self.entries["b"].get())
            x = _parse("x", self.entries["x"].get())
        except InputError as err:
            self._show(str(err), ERRC)
            return

        # 2) compute (domain / overflow errors handled with helpful messages)
        try:
            value = power_abx(a, b, x)
        except DomainError as err:
            self._show("Domain error:\n" + str(err), ERRC)
            return
        except OverflowGuard as err:
            self._show("Overflow:\n" + str(err), ERRC)
            return
        except Exception as err:                      # last-resort safety net
            self._show("Unexpected error: {0}".format(err), ERRC)
            return

        # 3) present the result in two formats (full precision + fixed)
        self._show(
            "{0} · {1} ^ {2}\n"
            "Full precision : {3!r}\n"
            "Fixed (10 dp)  : {4:.10f}".format(a, b, x, value, value),
            OKC,
        )


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
