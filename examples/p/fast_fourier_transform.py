"""
Fast Fourier Transform - Class P
================================
The Fast Fourier Transform (FFT) evaluates a polynomial at roots of unity much
faster than the naive O(n^2) approach. The Cooley-Tukey divide-and-conquer
algorithm splits the coefficients into even and odd parts and combines the
results efficiently.

FFT is in P because it runs in O(n log n) time. Using FFT for polynomial
multiplication also remains polynomial time.
"""

import cmath



def fft(values: list[complex], invert: bool = False) -> list[complex]:
    """Compute the discrete Fourier transform recursively."""
    n = len(values)
    if n == 1:
        return values[:]

    even_part = fft(values[0::2], invert)
    odd_part = fft(values[1::2], invert)
    angle = 2 * cmath.pi / n * (-1 if not invert else 1)
    root = complex(1.0, 0.0)
    root_step = cmath.exp(complex(0.0, angle))

    result = [0j] * n
    half = n // 2
    for index in range(half):
        term = root * odd_part[index]
        result[index] = even_part[index] + term
        result[index + half] = even_part[index] - term
        root *= root_step

    if invert:
        return [value / 2 for value in result]
    return result



def _next_power_of_two(n: int) -> int:
    """Return the smallest power of two that is at least n."""
    power = 1
    while power < n:
        power *= 2
    return power



def multiply_polynomials(first: list[int], second: list[int]) -> list[int]:
    """Multiply two polynomials with integer coefficients using FFT."""
    size = _next_power_of_two(len(first) + len(second) - 1)
    left = [complex(value, 0.0) for value in first] + [0j] * (size - len(first))
    right = [complex(value, 0.0) for value in second] + [0j] * (size - len(second))

    left_fft = fft(left)
    right_fft = fft(right)
    product_fft = [left_fft[i] * right_fft[i] for i in range(size)]
    product = fft(product_fft, invert=True)

    return [int(round(value.real)) for value in product[: len(first) + len(second) - 1]]


if __name__ == "__main__":
    first = [1, 2, 3]
    second = [4, 5, 6]
    product = multiply_polynomials(first, second)

    print(f"First polynomial coefficients: {first}")
    print(f"Second polynomial coefficients: {second}")
    print(f"Product coefficients: {product}")
