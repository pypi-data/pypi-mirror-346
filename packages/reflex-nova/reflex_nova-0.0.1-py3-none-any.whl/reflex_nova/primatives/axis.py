import reflex as rx
from .quantity import Qty

class Axis(rx.Base):
    """
    A coordinate axis defined by its name and orientation angle,
    specified in degrees or radians relative to the reference axis.
    """
    name: str
    quantity: Qty
    reference: 'Axis' = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)