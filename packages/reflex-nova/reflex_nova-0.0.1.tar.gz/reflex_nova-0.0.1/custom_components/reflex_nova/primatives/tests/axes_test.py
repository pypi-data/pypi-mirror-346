from reflex_nova.primatives.axes import x_axis, y_axis
import numpy as np

def test_x_axis():
    """Test the x-axis."""
    assert x_axis.name == "x"
    assert x_axis.quantity.value == 0.0
    assert x_axis.quantity.unit.selected == "rad"

def test_y_axis():
    """Test the y-axis."""
    assert y_axis.name == "y"
    assert y_axis.quantity.value == np.pi / 2
    assert y_axis.quantity.unit.selected == "rad"