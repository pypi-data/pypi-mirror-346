import reflex as rx
from .quantity import Qty
from .axis import Axis
from .axes import x_axis, y_axis
import numpy as np


class Force(rx.Base):
    """A class representing a force with magnitude and direction."""
    magnitude: Qty
    direction: Qty
    respect_to: Axis = x_axis

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


    @property
    def tail(self) -> list[float]:
        """Returns the tail of the force vector."""
        return [0.0, 0.0]
    
    @property
    def tip(self) -> list[float]:
        """Returns the tip of the force vector."""
        x = self.magnitude * np.cos(self.direction)
        y = self.magnitude * np.sin(self.direction)
        return [x.value, y.value]
    

#     def dict(self, *args, **kwargs):
#         data = super().dict(*args, **kwargs)
#         data['tail'] = self.tail
#         data['tip'] = self.tip
#         return data