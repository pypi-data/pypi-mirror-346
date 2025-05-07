from .axis import Axis
from .units import angle
from .quantity import Qty
import numpy as np


x_axis = Axis(
    name="x",
    quantity=Qty(
        value=0.0,
        unit=angle
    ),
)

y_axis = Axis(
    name="y",
    quantity=Qty(
        value=np.pi / 2,
        unit=angle
    ),
)

# def create_axis():