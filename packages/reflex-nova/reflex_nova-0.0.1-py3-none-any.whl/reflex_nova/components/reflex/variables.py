import reflex as rx
from typing import List, Optional, Union

class FrontendVar(rx.Base):
    """
    Representation of a variable for the frontend.
    """
    sym: str
    name: str
    disp: str
    # Either a value or an equation must be provided.
    eqn: Optional[Union[str, List]]
    val: Optional[float]
    # The unit of the variable and the options for the unit dropdown.
    unit: str
    unit_opts: List[str]
    # UI rendering attributes
    is_valid: bool = True
    error_msg: str = ""