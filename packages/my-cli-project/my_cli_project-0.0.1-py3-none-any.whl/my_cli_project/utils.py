# utils.py
def add(a, b):
    """Return the sum of a and b."""
    return a + b

def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

def factorial(n):
    """Return the factorial of n (non-recursive)."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def reverse_string(s):
    """Return the reversed version of the input string."""
    return s[::-1]
