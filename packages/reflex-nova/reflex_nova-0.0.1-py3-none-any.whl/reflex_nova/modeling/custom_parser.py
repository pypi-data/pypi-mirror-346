"""
custom_parser.py

This module defines a CustomParser class for parsing sympy expressions with automatic
transformations. A pre-configured parser instance is created as `parser` so that you can
directly import and use it in your project.
"""

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class CustomParser:
    """
    A custom parser for sympy expressions that applies pre-registered transformation
    functions after parsing.
    
    Attributes:
        local_dict (dict): A dictionary of local symbols/functions for parsing.
        transformations (list): A list of transformation functions to apply.
    """
    def __init__(self, local_dict=None, transformations=None):
        self.local_dict = local_dict if local_dict is not None else {}
        self.transformations = transformations if transformations is not None else []

    def register_transformation(self, transform_func):
        """
        Register a transformation function to be applied after parsing.
        
        Args:
            transform_func (callable): A function that accepts and returns a sympy.Expr.
        """
        self.transformations.append(transform_func)

    def parse(self, eqn, evaluate=False):
        """
        Parse an equation string into a sympy expression and apply all registered transformations.
        
        Args:
            eqn (str): The equation string.
            evaluate (bool): Whether to evaluate the parsed expression immediately.
        
        Returns:
            sympy.Expr: The transformed sympy expression.
        """
        expr = parse_expr(
            eqn,
            evaluate=evaluate,
            local_dict=self.local_dict,
            # transformations=standard_transformations + (implicit_multiplication_application,)
        )
        for transform in self.transformations:
            expr = transform(expr)
        return expr

def transform_cuberoot(expr):
    """
    Recursively transform any instance of x**(1/3) in the expression to cbrt(x).
    
    Args:
        expr (sympy.Expr): The input sympy expression.
        
    Returns:
        sympy.Expr: The expression with cube-root transformations applied.
    """
    # Define a symbolic cube-root function.
    cbrt_sym = sp.Function('cbrt')
    if expr.is_Pow and expr.exp.equals(sp.Rational(1, 3)):
        return cbrt_sym(transform_cuberoot(expr.base))
    elif expr.args:
        return expr.func(*[transform_cuberoot(arg) for arg in expr.args])
    else:
        return expr

# ------------------------------------------------------------------------------
# Pre-configured parser instance for the project.
# ------------------------------------------------------------------------------

# Define a local dictionary for parsing.
SYMPY_LOCAL_DICT = {
    'E': sp.Symbol('E'),
    'S': sp.Symbol('S'),
    'beta': sp.Symbol('beta'),
}

# Create the parser instance.
parser = CustomParser(local_dict=SYMPY_LOCAL_DICT)
# Pre-register the cube-root transformation.
parser.register_transformation(transform_cuberoot)

# You can register additional transformations here if needed.
