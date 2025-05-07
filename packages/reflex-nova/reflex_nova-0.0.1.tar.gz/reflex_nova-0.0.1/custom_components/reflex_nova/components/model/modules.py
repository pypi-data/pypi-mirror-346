import pint
import pint.facets
from pint.facets.numpy.numpy_func import _is_quantity, unwrap_and_wrap_consistent_units, _is_sequence_with_quantity_elements, implements
import pint.facets.numpy.quantity as quantity
import numpy as np
import warnings
from pint.facets.numpy import numpy_func, quantity
import inspect

# ####################################################################################################
# @implements("full_like", "function")
# def _full_like(a, fill_value, **kwargs):
#     if hasattr(fill_value, "_REGISTRY"):
#         units = fill_value.units
#         fill_value_ = fill_value.m
#     else:
#         units = None
#         fill_value_ = fill_value

#     magnitude = np.full_like(a.m, fill_value=fill_value_, **kwargs)
#     if units is not None:
#         return fill_value._REGISTRY.Quantity(magnitude, units)
#     else:
#         return magnitude

# for func_str in ["ones_like", "zeros_like", "empty_like"]:
#     numpy_func.implement_func("function", func_str, input_units=None, output_unit="match_input")

# numpy_func.nep35_function_names = set()

# def register_nep35_function(func_str):
#     numpy_func.nep35_function_names.add(func_str)

#     def wrapper(f):
#         return f

#     return wrapper

# numpy_func.register_nep35_function = register_nep35_function

# def implement_nep35_func(func_str):
#     # If NumPy is not available, do not attempt implement that which does not exist
#     if np is None:
#         return

#     func = getattr(np, func_str)

#     @numpy_func.register_nep35_function(func_str)
#     @implements(func_str, "function")
#     def implementation(*args, like, **kwargs):
#         args, kwargs = numpy_func.convert_to_consistent_units(*args, **kwargs)
#         result = func(*args, like=like.magnitude, **kwargs)
#         return like._REGISTRY.Quantity(result, like.units)
    
# numpy_func.implement_nep35_func = implement_nep35_func

# # generic implementations
# for func_str in {
#     "array",
#     "asarray",
#     "asanyarray",
#     "arange",
#     "ones",
#     "zeros",
#     "empty",
#     "identity",
#     "eye",
# }:
#     numpy_func.implement_nep35_func(func_str)

# @numpy_func.register_nep35_function("full")
# @implements("full", "function")
# def _full(shape, fill_value, dtype=None, order="C", *, like):
#     if hasattr(fill_value, "_REGISTRY"):
#         units = fill_value.units
#         fill_value_ = fill_value.m
#     else:
#         units = None
#         fill_value_ = fill_value

#     magnitude = np.full(
#         shape=shape,
#         fill_value=fill_value_,
#         dtype=dtype,
#         order=order,
#         like=like.magnitude,
#     )
#     if units is not None:
#         return fill_value._REGISTRY.Quantity(magnitude, units)
#     else:
#         return like._REGISTRY.Quantity(magnitude, units)
    
# @numpy_func.register_nep35_function("arange")
# @implements("arange", "function")
# def _arange(start, stop=None, step=None, dtype=None, *, like):
#     args = [start, stop, step]
#     if any(_is_quantity(arg) for arg in args):
#         args, kwargs = numpy_func.convert_to_consistent_units(
#             start,
#             stop,
#             step,
#             pre_calc_units=like.units,
#             like=like,
#         )
#     else:
#         kwargs = {"like": like.magnitude}

#     return like._REGISTRY.Quantity(np.arange(*args, dtype=dtype, **kwargs), like.units)

# @numpy_func.register_nep35_function("asarray")
# @implements("asarray", "function")
# def _asarray(a, dtype=None, order=None, *, like=None):
#     warnings.warn("This is a custom implementation of asarray.")
#     warnings.warn(f"a={a}", )
#     processed_choices, output_wrap = unwrap_and_wrap_consistent_units(*a)
#     warnings.warn(f"processed_choices={processed_choices}", )
#     warnings.warn(f"output_wrap={inspect.getsource(output_wrap)}", )
#     # If no "like" is provided, use the input if it is a pint quantity.
#     if like is None:
#         if hasattr(a, "_REGISTRY"):
#             like = a
#         else:
#             # Fallback to numpy if a isn’t a pint quantity.
#             return np.asarray(a, dtype=dtype, order=order)
#     # If a is a quantity, use its magnitude.
#     if _is_quantity(a):
#         a = a.magnitude
#     # Rewrap the result with the original units.
#     return like._REGISTRY.Quantity(np.asarray(a, dtype=dtype, order=order), like.units)

# def custom_array_function(self, func, types, args, kwargs):
#         nep35_functions = {getattr(np, name) for name in numpy_func.nep35_function_names}
#         if func in nep35_functions:
#             kwargs["like"] = self

#         return quantity.numpy_wrap("function", func, args, kwargs, types)

# quantity.NumpyQuantity.__array_function__ = custom_array_function


@implements("select", "function")
def _select(condlist, choicelist, default=0):
    # warnings.warn("This is a custom implementation of select.")
    # Remove units from each condition. (Conditions are expected to be boolean.)
    new_condlist = [
        c.magnitude if hasattr(c, "magnitude") else c
        for c in condlist
    ]
    # Process the choices and default together.
    # This returns a tuple of processed choices and an output wrapper.
    all_choices = list(choicelist)
    if default is not None:
        all_choices.append(default)
    processed_choices, output_wrap = unwrap_and_wrap_consistent_units(*all_choices)

    # Since processed_choices is a tuple, extract the default via indexing.
    if default is not None:
        processed_default = processed_choices[-1]
        processed_choices = processed_choices[:-1]
    else:
        processed_default = 0

    # Call the NumPy select function on the processed (unit-stripped) inputs.
    result_magnitude = np.select(new_condlist, processed_choices, default=processed_default)

    # Rewrap the result with the proper unit.
    return output_wrap(result_magnitude)

# _original_asarray = np.asarray

# def custom_asarray(*args, **kwargs):
#     print("CUSTOM ASARRAY")
#     print(args)
#     print(kwargs)
#     # if hasattr(a, "_REGISTRY"):
#         # return _asarray(a, dtype=dtype, order=order, like=a)
#     return _original_asarray(*args, **kwargs)

# np.asarray = custom_asarray

# https://github.com/hgrecco/pint/pull/1669/files#diff-3902d8460bf42f38121b360a0cf397597567077c08aa6d0a565a65332290395c

_original_asarray = np.asarray

def custom_asarray(a, **kwargs):
    # If a is a list of quantity objects just return the list
    if all(hasattr(item, "_REGISTRY") for item in a):
        return a
    return _original_asarray(a, **kwargs)

np.asarray = custom_asarray

_original_amin = np.amin

def custom_amin(a, **kwargs):
    # If a is a list of quantity objects, built in min will work
    if all(hasattr(item, "_REGISTRY") for item in a):
        return min(a)
    else:
        return _original_amin(a, **kwargs)
    
np.amin = custom_amin

_original_amax = np.amax

def custom_amax(a, **kwargs):
    # If a is a list of quantity objects, built in max will work
    if all(hasattr(item, "_REGISTRY") for item in a):
        return max(a)
    else:
        return _original_amax(a, **kwargs)
    
np.amax = custom_amax

modules = [
    'numpy',   
]
