#!/usr/bin/env python3
"""
SOEN 6011 - Summer 2026 - Deliverable 2, Problem 5
Custom exception classes for the F5 calculator: f(x) = a * b^x.


"""


class CalculatorError(Exception):
    """Base class for all errors raised by the F5 calculator."""


class DomainError(CalculatorError):
    """
    Raised when an input lies outside the function's domain.

    For F5 (a * b^x) the only domain restriction is b > 0: a non-positive
    base raised to a fractional power is not a real number.
    """


class OverflowGuard(CalculatorError):
    """Raised when a result exceeds the representable floating-point range."""


class InputError(CalculatorError):
    """
    Raised when a user-entered value cannot be interpreted as a real number,
    or a required field is empty. Carries the field name so the interface can
    tell the user exactly which input to fix.
    """

    def __init__(self, field, raw):
        self.field = field
        self.raw = raw
        if raw == "":
            message = "The field '{0}' is empty. Please enter a number.".format(field)
        else:
            message = (
                "'{0}' is not a valid number for '{1}'. Please enter a value "
                "such as 2, -3.5, or 1e3.".format(raw, field)
            )
        super().__init__(message)
