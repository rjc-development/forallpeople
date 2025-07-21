from fractions import Fraction
import math
import pytest
import forallpeople as si
import forallpeople.physical_helper_functions as phf

si.environment("test_definitions", top_level=True)


def test__auto_prefix_mandates():
    func = phf._auto_prefix
    dims = si.Dimensions
    assert func(1500, dims(1, 2, -2, 0, 0, 0, 0), 1) == "k"
    assert func(2400000, dims(1, 2, -2, 0, 0, 0, 0), 1) == "k"
    assert func(2000, dims(1, 2, -2, 0, 0, 0, 0), 2) == ""
    assert func(1234567, dims(1, 2, -3, 0, 0, 0, 0), 1) == "M"
    assert func(1234567890, dims(1, -1, -2, 0, 0, 0, 0), 1) == "M"

def test___float__():
    assert float(100 * m) == pytest.approx(100)
    assert float(52.5 * kN) == pytest.approx(52.5)
    assert float(3400 * N) == pytest.approx(3.4)
    assert float(1e10 * kg / m / s**2) == pytest.approx(10000)