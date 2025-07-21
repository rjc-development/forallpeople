from fractions import Fraction
import math
import pytest
import forallpeople as si
import forallpeople.physical_helper_functions as phf

si.environment("structural_copy", top_level=True)

### Testing parameters ###
env_dims = si.environment.units_by_dimension
env_fact = si.environment.units_by_factor
units = {
    "A": 0.05 * kg,
    "B": 3.2e-3 * m,
    "C": 1000 * ft,
    "D": 1e6 * N,
    "E": 0.2 * kip,
    "F": 5 * N * 1e3 * kip,
}
parameters = [
    (value, phf._powers_of_derived(value.dimensions, env_dims))
    for value in units.values()
]

def test__evaluate_dims_and_factor():
    func = phf._evaluate_dims_and_factor

    # Defined unit with a default and the defined unit factor is a match
    # (passes through without swap)
    assert func(
        si.Dimensions(1, 1, -2, 0, 0, 0, 0),
        1 / Fraction("0.45359237") / Fraction("9.80665") / 1000,
        1,
        env_fact,
        env_dims,
    ) == ("kip", False, 1 / Fraction("0.45359237") / Fraction("9.80665") / 1000)

    # Defined unit with a default and the defined unit factor is not a match
    # (swapped)
    assert func(
        si.Dimensions(1, 1, -2, 0, 0, 0, 0),
        1 / Fraction("0.45359237") / Fraction("9.80665") / 900,
        1,
        env_fact,
        env_dims,
    ) == ("lb", False, 1 / Fraction("0.45359237") / Fraction("9.80665"))

    # Derived unit to a power
    assert func(si.Dimensions(1, 1, -2, 0, 0, 0, 0), 1, 2, env_fact, env_dims) == (
        "N",
        True,
        1,
    )
    # Derived unit power of one
    assert func(si.Dimensions(1, 1, -2, 0, 0, 0, 0), 1, 1, env_fact, env_dims) == (
        "N",
        True,
        1,
    )
    # Defined unit that is not a default unit
    assert func(
        si.Dimensions(0, 1, 0, 0, 0, 0, 0),
        12 / Fraction("0.3048"),
        1,
        env_fact,
        env_dims,
    ) == ("inch", False, 12 / Fraction("0.3048"))

    # Single dimension base unit
    assert func(si.Dimensions(1, 0, 0, 0, 0, 0, 0), 1, 3, env_fact, env_dims) == (
        "",
        True,
        1,
    )

    # Not defined in environment
    assert func(si.Dimensions(1, 1, 1, 0, 0, 0, 0), 1, 1, env_fact, env_dims) == (
        "",
        False,
        1,
    )