import reflex as rx
from typing import List, Optional, Callable, Union
import pint
import numpy as np

class ModelVar(rx.Base):
    """
    Internal representation of a model variable with computation details.
    """
    sym: str
    # Either a value or an equation must be provided.
    eqn: Optional[Union[str, List]]
    val: Optional[Union[float, np.ndarray]]
    # The unit of the variable.
    unit: str
    # The pint Quantity object for the variable.
    qty: Optional[pint.Quantity]
    # The names of variables on which this one depends.
    deps: Optional[List[str]]
    # The callable that computes the variable.
    eq_func: Optional[Callable]
    # The LaTeX representation of the equation.
    eq_tex: Optional[str]