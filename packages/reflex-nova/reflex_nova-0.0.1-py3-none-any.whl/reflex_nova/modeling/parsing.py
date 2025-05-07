import sympy as sp
from typing import Callable, List, Set, Tuple

from .custom_parser import parser
from ..components.model.modules import modules


# Global dictionary of pre-defined symbols for parsing.
SYMPY_LOCAL_DICT = {
    'E': sp.Symbol('E'),
    'S': sp.Symbol('S'),
    'beta': sp.Symbol('beta'),
}

def _extract_equation_components(equation: str) -> Tuple[sp.Expr, sp.Expr, Set[sp.Symbol], sp.Symbol]:
    """
    Parse an equation string in the form "computed_var == expression" (or vice versa)
    and extract the full parsed equality, the computed expression, the independent symbols,
    and the computed (dependent) symbol.
    
    Parameters:
        equation (str): The equation string to parse.
    
    Returns:
        Tuple containing:
            - full_eq (sp.Expr): The complete parsed equality.
            - computed_expr (sp.Expr): The expression computing the variable.
            - input_syms (Set[sp.Symbol]): The set of independent symbols (from the expression side).
            - computed_sym (sp.Symbol): The dependent symbol.
    
    Raises:
        ValueError: If the equation is not in the proper equality format.
    """
    full_eq = parser.parse(equation)
    if not isinstance(full_eq, sp.Equality):
        raise ValueError("Equation must be in the form 'variable == expression'.")
    
    lhs_syms = list(full_eq.lhs.free_symbols)
    rhs_syms = list(full_eq.rhs.free_symbols)
    
    if len(lhs_syms) == 1 and len(rhs_syms) >= 1:
        computed_sym = lhs_syms[0]
        computed_expr = full_eq.rhs
        input_syms = full_eq.rhs.free_symbols
    elif len(lhs_syms) >= 1 and len(rhs_syms) == 1:
        computed_sym = rhs_syms[0]
        computed_expr = full_eq.lhs
        input_syms = full_eq.lhs.free_symbols
    else:
        raise ValueError(
            "Invalid equation format. Expected a single computed variable defined in terms of one or more input variables."
        )
    
    return full_eq, computed_expr, input_syms, computed_sym


def parse_equation(equation: str) -> Tuple[List[str], Callable, str]:
    """
    Parse a single equation string into a lambdified function, a list of input variable names,
    and a LaTeX representation.

    The equation must be provided in the form:
        "computed_var == expression"
    where the left-hand side is the computed (dependent) variable and the right-hand side
    is an expression in one or more input (independent) variables.

    Parameters:
        equation (str): The equation string to parse.

    Returns:
        Tuple[List[str], Callable, str]:
            - A list of input variable names (as strings) on which the equation depends.
            - A callable function (via lambdify) that computes the expression.
            - A LaTeX string representing the full equation.

    Raises:
        ValueError: If the equation is not in the proper format.
    """
    try:
        full_eq, computed_expr, input_syms, _ = _extract_equation_components(equation)
        # Build a sorted list of independent variable names.
        input_vars = sorted({str(sym) for sym in input_syms})
        # Create the lambdified function using the computed expression.
        lambda_func = sp.lambdify(list(input_syms), computed_expr, modules=modules)
        # Generate a LaTeX representation of the full equation.
        latex_str = sp.latex(full_eq, mul_symbol=' \\cdot ')
    except Exception as error:
        raise ValueError(f"Error processing equation '{equation}': {error}") from error

    return input_vars, lambda_func, latex_str


def parse_piecewise_equation(branches: List[Tuple[str, str]]) -> Tuple[List[str], Callable, str]:
    """
    Construct a piecewise expression from branch definitions and lambdify it.

    Each branch is defined by a tuple (condition_str, equation_str) where:
      - condition_str: A string representing the branch condition.
      - equation_str: A string representing the branch equation in the form "computed_var == expression".

    This function parses each branch (using the common equation parser logic), extracts the computed
    expression and condition, and then constructs a piecewise expression. The independent symbols are
    collected from all branches (excluding the computed symbols). Optionally, unsafe division operations
    can be replaced (e.g., via a 'replace_div' function).

    Parameters:
        branches (List[Tuple[str, str]]):
            A list of branch definitions. Each branch is a tuple containing:
                - condition_str: The condition as a string.
                - equation_str: The equation in the form "variable == expression".

    Returns:
        Tuple[List[str], Callable, str]:
            - A sorted list of input variable names (as strings) required by the piecewise expression.
            - A callable function (via lambdify) that evaluates the piecewise expression.
            - A LaTeX string representing the piecewise expression.

    Raises:
        ValueError: If any branch equation is not in the proper "variable == expression" format.
    """
    branch_exprs = []
    overall_input_syms: Set[sp.Symbol] = set()
    output_syms: Set[sp.Symbol] = set()

    for cond_str, eq_str in branches:
        # Parse the branch condition.
        condition_expr = parser.parse(cond_str)
        # Parse the branch equation using the common helper.
        _, computed_expr, input_syms, computed_sym = _extract_equation_components(eq_str)
        output_syms.add(computed_sym)
        overall_input_syms.update(input_syms)
        branch_exprs.append((computed_expr, condition_expr))

    # Exclude any output symbols from the set of overall inputs.
    input_vars = sorted({str(sym) for sym in overall_input_syms if sym not in output_syms})

    # (Optional) Replace unsafe division operations if necessary.
    # safe_branches = [(replace_div(expr), cond) for expr, cond in branch_exprs]
    # For now, use branch_exprs directly.
    piecewise_expr = sp.Piecewise(*branch_exprs)

    lambda_func = sp.lambdify(input_vars, piecewise_expr, modules=modules)
    latex_str = sp.latex(piecewise_expr, mul_symbol=' \\cdot ')

    return input_vars, lambda_func, latex_str
