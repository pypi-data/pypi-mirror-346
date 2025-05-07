import reflex as rx
from pydantic import computed_field
from typing import Optional, List
from .force import Force
from .axes import Axis, global_x_axis, global_y_axis

def _default_forces() -> list[Force]:
    # if you really want a starter Force, put it here;
    # otherwise return [] and add via add_force()
    return [
        Force(mag=2, mag_unit="kN", dir=-45, dir_unit='deg', respect_to=global_x_axis),
        Force(mag=6, mag_unit="kN", dir=240, dir_unit='deg', respect_to=global_x_axis)
    ]

def _default_axes() -> List[Axis]:
    return [global_x_axis, global_y_axis]

class Body(rx.Base):
    """Class to represent a body or node where forces are applied."""
    forces: Optional[list[Force]]
    resultant: Optional[Force]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.forces is None:
            self.forces = _default_forces()

    # def add_force(self, force: Force) -> None:
    #     """Add a force to the free body diagram."""
    #     self.forces.append(force)