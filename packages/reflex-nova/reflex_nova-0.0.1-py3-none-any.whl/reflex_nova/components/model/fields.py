import reflex as rx
from typing import List, Optional, Callable, Union
import pint
import numpy as np
from .units import Units

class IndependentVar(str):
    sym: str
    name: str
    disp: str
    value: float
    unit: Units
    doc: str
    def __new__(cls, sym, *, name, value, unit, doc) -> "IndependentVar":
        obj = super().__new__(cls, sym)
        obj.sym = sym
        obj.name = name
        obj.disp = sym
        obj.value = value
        obj.unit = unit
        obj.doc = doc
        return obj
    
class DependentVar(str):
    sym: str
    name: str
    disp: str
    eqn: Union[str, List]
    unit: Units
    doc: str
    def __new__(cls, sym, *, name, eqn, unit, doc) -> "DependentVar":
        obj = super().__new__(cls, sym)
        obj.sym = sym
        obj.name = name
        obj.disp = sym
        obj.eqn = eqn
        obj.unit = unit
        obj.doc = doc
        return obj
    
