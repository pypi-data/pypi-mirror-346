from ..components.model.modules import modules


import sympy as sp
import numpy as np
from ..components.model.units import Q_
from ..modeling.topological_model import parse_piecewise_equation
import inspect
import pytest
from pint.testsuite import helpers

# import unyt as u
from pint.facets.numpy import numpy_func
from pint.testsuite import test_numpy

# Silence NEP 18 warning
# import warnings

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     Q_([])

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from sympy import Function

# Optional: define a transform to convert x**(1/3) to cbrt(x)
def convert_pow_to_cbrt(expr):
    if expr.is_Pow and expr.exp == sp.Rational(1, 3):
        return sp.cbrt(convert_pow_to_cbrt(expr.base))
    elif expr.args:
        return expr.func(*[convert_pow_to_cbrt(arg) for arg in expr.args])
    else:
        return expr

def parse_with_cbrt(eqn_str):
    expr = parse_expr(
        eqn_str,
        evaluate=False,
        transformations=standard_transformations + (implicit_multiplication_application,)
    )
    return convert_pow_to_cbrt(expr)

cbrt_sym = sp.Function('cbrt')

def transform_cuberoot(expr):
    """
    Recursively transform Pow(x, 1/3) in expr to cbrt(x)
    """
    # If expr is a power and the exponent equals 1/3, replace with cbrt(x)
    if expr.is_Pow and expr.exp.equals(sp.Rational(1, 3)):
        return cbrt_sym(transform_cuberoot(expr.base))
    # Otherwise, if expr has subexpressions, apply recursively.
    elif expr.args:
        return expr.func(*[transform_cuberoot(arg) for arg in expr.args])
    else:
        return expr

def test_asarray(capsys):
    x = Q_(1, "m")
    y = Q_(4, "mm")
    actual = np.asarray([x, y])


    with capsys.disabled():
        print('')
        print("ACTUAL", actual)


# Prints ACTUAL [[1 2 3] [4 5 6]]

def test_min(capsys):
    # Define the equation as a string with a max function.
    eqn = "L_4 == min(2.5*(T_h - c_h), 2.5*(T_b - c_b) + T_r)"

    # Parse the expression without evaluating it.
    parsed_eqn = sp.parse_expr(eqn, evaluate=False)
    latex_eqn = sp.latex(parsed_eqn, mul_symbol=' \\cdot ')

    # Create the lambda function using our modules mapping.
    lambda_eqn = sp.lambdify(
        list(parsed_eqn.rhs.free_symbols),
        parsed_eqn.rhs,
        modules=modules
    )

    context = {
        'T_h': Q_(100, 'mm'),
        'c_h': Q_(1, 'mm'),
        'T_b': Q_(50, 'mm'),
        'c_b': Q_(1, 'mm'),
        'T_r': Q_(50, 'mm')
    }


    with capsys.disabled():
        # print(hasattr(numpy_func, "register_nep35_function"))  # Should output: True

        # print(inspect.getsource(lambda_eqn))
        result = lambda_eqn(**context)
        print("RESULT", result)
        # try_result = lambda_eqn(**try_context)
        # print("TRY RESULT", try_result)

    # assert result == Q_(247.5, 'mm')

        # print(np.asarray([1*mm, 2*mm, 3*mm]))

def test_cbrt(capsys):
    # "{c_t} == cbrt({c_r} - sqrt({c_q}**3 + {c_r}**2))"
    eqn = "c_t == cbrt(c_r - sqrt(c_q**3 + c_r**2))"

    local_dict = {"cbrt": sp.cbrt}
    # Parse the expression without evaluating it.
    parsed_eqn = parsed_eqn = parse_with_cbrt(eqn)
    parsed_eqn = transform_cuberoot(parsed_eqn)

    latex_eqn = sp.latex(parsed_eqn, mul_symbol=' \\cdot ')

    # Create the lambda function using our modules mapping.
    lambda_eqn = sp.lambdify(
        list(parsed_eqn.rhs.free_symbols),
        parsed_eqn.rhs,
        modules=modules
    )

    context = {
        'c_r': Q_(-779, 'm**3/s**3'),
        'c_q': Q_(20.6, 'm**2/s**2'),
    }

    with capsys.disabled():
        # print(hasattr(numpy_func, "register_nep35_function"))  # Should output: True
        print("PARSING", parsed_eqn)
        print(sp.srepr(parsed_eqn))

        print(inspect.getsource(lambda_eqn))
        result = lambda_eqn(**context)
        print("RESULT", result)
        # try_result = lambda_eqn(**try_context)
        # print("TRY RESULT", try_result)

def test_max(capsys):
    # Define the equation as a string with a max function.
    eqn = "L_4 == max(2.5*(T_h - c_h), 2.5*(T_b - c_b) + T_r)"

    # Parse the expression without evaluating it.
    parsed_eqn = sp.parse_expr(eqn, evaluate=False)
    latex_eqn = sp.latex(parsed_eqn, mul_symbol=' \\cdot ')

    # Create the lambda function using our modules mapping.
    lambda_eqn = sp.lambdify(
        list(parsed_eqn.rhs.free_symbols),
        parsed_eqn.rhs,
        modules=modules
    )

    context = {
        'T_h': Q_(100, 'mm'),
        'c_h': Q_(1, 'mm'),
        'T_b': Q_(50, 'mm'),
        'c_b': Q_(1, 'mm'),
        'T_r': Q_(50, 'mm')
    }


    with capsys.disabled():
        # print(hasattr(numpy_func, "register_nep35_function"))  # Should output: True

        # print(inspect.getsource(lambda_eqn))
        result = lambda_eqn(**context)
        print("RESULT", result)
        # try_result = lambda_eqn(**try_context)
        # print("TRY RESULT", try_result)

    # assert result == Q_(247.5, 'mm')

        # print(np.asarray([1*mm, 2*mm, 3*mm]))


@pytest.mark.filterwarnings("ignore:divide by zero encountered in divide:RuntimeWarning")
@pytest.mark.filterwarnings("ignore:divide by zero encountered in log:RuntimeWarning")
@pytest.mark.filterwarnings("ignore:invalid value encountered in subtract:RuntimeWarning")
def test_piecewise(capsys):
    eqn = [
        ("r == 0", "G_11 == 0"),
        ("r_o == 0", "G_11 == 1/64"),
        ("r <= r_o", "G_11 == (1/64) * (1 + 4 * (r_o/r)**2 - 5 * (r_o/r)**4 - 4 * (r_o/r)**2 * (2 + (r_o/r)**2) * log(r/r_o)) * (0)**0"),
        ("r > r_o", "G_11 == (1/64) * (1 + 4 * (r_o/r)**2 - 5 * (r_o/r)**4 - 4 * (r_o/r)**2 * (2 + (r_o/r)**2) * log(r/r_o)) * (r - r_o)**0")
    ]

    vars, parsed_eqn, latex_eqn = parse_piecewise_equation(eqn)

    context = {
        'r': Q_([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 'mm'),
        'r_o': Q_(10, 'mm')
    }

    result = parsed_eqn(**context)

    with capsys.disabled():
        print("RESULT", result)

