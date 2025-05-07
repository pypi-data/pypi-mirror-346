import pint
import reflex as rx
import numpy as np
from .axes import Axis, global_x_axis, global_y_axis
from pydantic import computed_field
from reflex_nova.primatives import Unit, ureg

class Qty(rx.Base):
    value: float
    unit: Unit

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __add__(self, other: 'Qty') -> 'Qty':
        if self.unit == other.unit:
            return Qty(value=self.value + other.value, unit=self.unit)
        else:
            sum = self.quantity + other.quantity
            return Qty(value=sum.magnitude, unit=sum.units)

    # def __str__(self) -> str:
    #     return f"{self.value} {self.unit}"
    
    # def __repr__(self) -> str:
    #     return str(self)
    
    @property
    def quantity(self) -> pint.Quantity:
        """Returns the quantity as a float."""
        return ureg.Quantity(self.value, self.unit)
    
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data['quantity'] = self.quantity
        return data
    


# class Force(rx.Base):
#     """A class representing a force with magnitude and direction."""
#     mag: float
#     mag_unit: str
#     dir: float
#     dir_unit: str
#     respect_to: Axis = global_x_axis

#     def __add__(self, other: 'Force') -> 'Force':
#         x = self.x + other.x
#         y = self.y + other.y
#         mag = np.sqrt(x**2 + y**2)
#         dir = np.arctan2(y, x)
#         return Force(
#             mag=mag.magnitude,
#             mag_unit=self.mag_unit, dir=dir, dir_unit=self.dir_unit)

#     @property
#     def x(self) -> float:
#         """Returns the x-component of the force."""
#         return self.mag_qty * np.cos(self.dir_qty)
    
#     @property
#     def y(self) -> float:
#         """Returns the y-component of the force."""
#         return self.mag_qty * np.sin(self.dir_qty)
    
#     @property
#     def mag_qty(self) -> float:
#         """Returns the magnitude of the force."""
#         return Q_(self.mag, self.mag_unit)
    
#     @property
#     def dir_qty(self) -> float:
#         """Returns the direction of the force."""
#         return Q_(self.dir, self.dir_unit)


#     @property
#     def tail(self) -> list[float]:
#         """Returns the tail of the force vector."""
#         return [0.0, 0.0]
    
#     @property
#     def tip(self) -> list[float]:
#         """Returns the tip of the force vector."""
#         x = self.mag_qty * np.cos(self.dir_qty)
#         y = self.mag_qty * np.sin(self.dir_qty)
#         return [x.magnitude, y.magnitude]
    

#     def dict(self, *args, **kwargs):
#         data = super().dict(*args, **kwargs)
#         data['tail'] = self.tail
#         data['tip'] = self.tip
#         return data
    


