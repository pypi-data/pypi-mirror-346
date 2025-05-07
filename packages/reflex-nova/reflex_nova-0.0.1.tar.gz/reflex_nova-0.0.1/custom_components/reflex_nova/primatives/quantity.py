import reflex as rx
import pint
from .unit import Unit, ureg
from .units import dimensionless
import numpy as np
from .nums import are_close_enough
from typing import Union

class Qty(rx.Base):
    """A class representing a quantity with a value and unit."""
    value: float
    unit: Unit

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __eq__(self, other: 'Qty') -> bool:
        if self is other:
            return True

        if not isinstance(other, Qty):
            return False
        
        return are_close_enough(self, other)
        
    def __add__(self, other: 'Qty') -> 'Qty':
        if self.unit == other.unit:
            return Qty(value=self.value + other.value, unit=self.unit)
        else:
            added = (self.qty_as_pint() + other.qty_as_pint())
            return Qty(value=float(added.m), unit=Unit(selected=str(added.u), options=self.unit.options))
        
    def __sub__(self, other: 'Qty') -> 'Qty':
        if self.unit == other.unit:
            return Qty(value=self.value - other.value, unit=self.unit)
        else:
            subtracted = (self.qty_as_pint() - other.qty_as_pint())
            return Qty(value=float(subtracted.m), unit=Unit(selected=str(subtracted.u), options=self.unit.options))
        
    def __mul__(self, other: Union["Qty", int, float]) -> "Qty":
        # 1) figure out the pint.Quantity for each operand
        if isinstance(other, Qty):
            q_self  = self.qty_as_pint()
            q_other = other.qty_as_pint()
        elif isinstance(other, (int, float)):
            # treat a bare number as dimensionless
            q_self  = self.qty_as_pint()
            q_other = self.qty_as_pint()._REGISTRY.Quantity(other, self.qty_as_pint().units.dimensionality)  # or simply ureg.Quantity(other, "Ø")
        else:
            return NotImplemented

        # 2) let Pint multiply & convert automatically
        result_q = q_self * q_other

        # 3) defer to Unit.__mul__ for all the unit-option work
        new_unit = self.unit * (other.unit if isinstance(other, Qty) else dimensionless)

        # 4) express the result in the “selected” of your new_unit
        #    (e.g. if new_unit.selected=="m²", this gives you the number in m²)
        val = float(result_q.to(new_unit.selected).magnitude)

        return Qty(value=val, unit=new_unit)
        
    def __repr__(self):
        return f"Qty(value={self.value}, unit={self.unit})"
    
    def __str__(self):
        return f"{self.value} {self.unit.selected}"

    def qty_as_pint(self) -> pint.Quantity:
        """Convert the quantity to a Pint Quantity."""
        return ureg.Quantity(self.value, self.unit.selected)
    
    def cos(self) -> pint.Quantity:
        """Calculate the cosine of the quantity."""
        value = np.cos(self.qty_as_pint())
        return Qty(value=float(value.m), unit=dimensionless)
    
    def sin(self) -> pint.Quantity:
        """Calculate the sine of the quantity."""
        value = np.sin(self.qty_as_pint())
        return Qty(value=float(value.m), unit=dimensionless)
    
    def fabs(self) -> pint.Quantity:
        """Calculate the absolute value of the quantity."""
        value = np.fabs(self.qty_as_pint())
        return Qty(value=float(value.m), unit=self.unit)
    
    def __lt__(self, other: 'Qty') -> bool:
        """Less than comparison."""
        if isinstance(other, Qty):
            return self.qty_as_pint() < other.qty_as_pint()
        elif isinstance(other, (int, float)):
            return self.qty_as_pint().m < other
        else:
            return NotImplemented
        
    def convert_to(self, unit: str) -> 'Qty':
        """Convert the quantity to a different unit."""
        if self.unit == unit:
            return self
        else:
            qty_converted = self.qty_as_pint().to(unit)
            new_unit = Unit(selected=unit, options=self.unit.options)
            return Qty(value=float(qty_converted.m), unit=new_unit)

    def update_unit(self, new_unit: str):
        """Update the unit and convert the value accordingly."""
        pint_qty = self.qty_as_pint().to(new_unit)
        self.value = float(pint_qty.m)
        self.unit.update_selected(new_unit)

    def pint_as_qty(self, _pint: pint.Quantity) -> 'Qty':
        """Convert pint quantity to Qty."""
        _pint = _pint.to(self.unit.selected)
        return Qty(value=float(_pint.m), unit=self.unit)
        