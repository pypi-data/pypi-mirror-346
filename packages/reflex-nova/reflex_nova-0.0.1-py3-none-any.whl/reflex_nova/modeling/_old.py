# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

# local_dict = {
#     'E': sp.Symbol('E'),
#     'S': sp.Symbol('S'),
#     'beta': sp.Symbol('beta'),
# }

# Create or import your pint unit registry.
# ureg = pint.UnitRegistry()

# def safe_div(
#     x: Union[np.ndarray, float, Q_],
#     y: Union[np.ndarray, float, Q_]
# ) -> Union[np.ndarray, float, Q_]:
#     """
#     Safely perform division x / y element-wise while preserving pint units if present.
    
#     The division is computed only where y != 0; np.inf is returned where y == 0.
    
#     Parameters:
#         x: Numerator (scalar, numpy array, or Q_).
#         y: Denominator (scalar, numpy array, or Q_).

#     Returns:
#         The result of the division, with division-by-zero replaced by np.inf,
#         and with units preserved if x and/or y are Q_.
#     """
#     # Check if x and/or y are Q_ and extract magnitudes and units.
#     if isinstance(x, Q_):
#         x_val = np.asarray(x.magnitude)
#         x_unit = x.units
#     else:
#         x_val = np.asarray(x)
#         x_unit = None

#     if isinstance(y, Q_):
#         y_val = np.asarray(y.magnitude)
#         y_unit = y.units
#     else:
#         y_val = np.asarray(y)
#         y_unit = None

#     # Determine the resulting unit.
#     if x_unit is not None and y_unit is not None:
#         result_unit = x_unit / y_unit
#     elif x_unit is not None:
#         result_unit = x_unit
#     elif y_unit is not None:
#         result_unit = 1 / y_unit
#     else:
#         result_unit = None

#     # Determine an appropriate dtype for the result.
#     result_dtype = np.result_type(x_val, y_val, np.float64)
#     result = np.empty_like(x_val, dtype=result_dtype)

#     # Perform the division only where y is not zero.
#     np.divide(x_val, y_val, out=result, where=(y_val != 0))
#     result = np.where(y_val == 0, np.inf, result)

#     # Wrap the result with Q_ if a unit is available.
#     if result_unit is not None:
#         try:
#             result = Q_(result, result_unit)
#         except Exception as e:
#             raise ValueError(f"Error creating Quantity with unit '{result_unit}': {e}") from e
    
#     # If the result is a scalar, return it as a scalar.
#     return result



# def safe_log(x: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
#     """
#     Safely compute the natural logarithm of x.
    
#     Computes np.log(x) and replaces the result with 0.0 where x is infinite.

#     Parameters:
#         x: Input value(s) (scalar or numpy array).

#     Returns:
#         The natural logarithm of x, with np.inf inputs replaced by 0.0.
#     """
#     x_arr = np.asarray(x)
#     result = np.log(x_arr)
#     result[np.isinf(x_arr)] = 0.0
#     return result if result.size > 1 else result[0]

# def safe_select(
#     conditions: np.ndarray,
#     choices: np.ndarray,
#     default: Union[np.ndarray, float, Q_]
# ) -> Union[np.ndarray, float, Q_]:
#     """
#     Safely select elements from choices based on conditions, with a default value.
    
#     This function is similar to np.select, but it ensures that the default value
#     is returned with the correct units if the conditions do not match any choice.
#     """
#     # Convert all choice to base units
#     new_choices = []
#     units = []
#     for choice in choices:
#         if isinstance(choice, Q_):
#             new_choices.append(choice.to_base_units().magnitude)
#             units.append(choice.units)
#         else:
#             new_choices.append(choice)
#         # choices = [choice.to_base_units().magnitude for choice in choices]
#         # print(choices)
#         # units = [choice.units for choice in choices]
#     mag_result = np.select(conditions, new_choices, default=default)

#     if units:
#         for unit in units:
#             if unit.dimensionality != units[0].dimensionality:
#                 raise ValueError("All choices must have the same units.")
    
#         unit = units[0]
#         try:
#             result = Q_(mag_result, unit)
#         except Exception as e:
#             raise ValueError(f"Error creating Quantity with unit '{unit}': {e}") from e
#     else:
#         result = Q_(mag_result, 'dimensionless')
    
#     return result



# def replace_div(expr: sp.Expr) -> sp.Expr:
#     """
#     Recursively replace divisions in a sympy expression with calls to a safe division function.
    
#     This function traverses the expression tree and replaces any division operation
#     (including those implied via multiplication by a negative power) with a call to
#     `safe_div` so that, after lambdification, division-by-zero is handled safely.

#     Parameters:
#         expr: A sympy expression.

#     Returns:
#         A sympy expression with all divisions replaced by calls to safe_div.
#     """
#     # Avoid reprocessing if already wrapped in sdiv
#     if expr.is_Function and expr.func.__name__ == "safe_div":
#         return expr

#     # Base case: atoms are returned as-is.
#     if expr.is_Atom:
#         return expr

#     # Process additions recursively.
#     if expr.is_Add:
#         return sp.Add(*[replace_div(arg) for arg in expr.args])

#     # Process multiplications: check if the expression represents a division.
#     if expr.is_Mul:
#         num, den = expr.as_numer_denom()
#         if den != 1:
#             return sp.Function('safe_div')(replace_div(num), replace_div(den))
#         return sp.Mul(*[replace_div(arg) for arg in expr.args])

#     # Process powers.
#     if expr.is_Pow:
#         # If exponent is -1, interpret as division.
#         if expr.exp == -1:
#             return sp.Function('safe_div')(1, replace_div(expr.base))
#         return sp.Pow(replace_div(expr.base), replace_div(expr.exp))

#     # Process function arguments.
#     if expr.is_Function:
#         return expr.func(*[replace_div(arg) for arg in expr.args])

#     # Fallback: return the expression as-is.
#     return expr