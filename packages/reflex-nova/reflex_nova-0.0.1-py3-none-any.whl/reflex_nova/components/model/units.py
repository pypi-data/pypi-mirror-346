import pint
import fractions
import sympy as sp
import reflex as rx
from typing import List, Optional, Union
# =============================================================================
# Initialize Pint Unit Registry
# =============================================================================
u = pint.UnitRegistry()
Q_ = u.Quantity

u.define("dless = 1 = Ø")

def format_unit(unit: pint.Unit) -> str:
    """
    Returns f"{dim:~P}" if no fractional exponent exists,
    and f"{dim:~D}" if a fractional exponent is present.
    """
    pretty = f"{unit:~P}"
    # If the pretty format contains the Unicode dot (⋅), a fractional exponent exists.
    if "⋅" in pretty:
        return f"{unit:~D}"
    return pretty

def format_units(units: List[pint.Unit]) -> List[str]:
    return [format_unit(unit) for unit in units]

class Units:
    si: str
    imp: str
    opts: List[str]

    def __init__(self, si: pint.Unit, imp: pint.Unit, opts: List[pint.Unit]):
        self.si = format_unit(si)
        self.imp = format_unit(imp)
        self.opts = format_units(opts)

    # class Config:
    #     frozen = True

angle = Units(
    si=u.radian,
    imp=u.degree,
    opts = [u.radian, u.deg]
)

dimensionless = Units(
    si=u.dimensionless,
    imp=u.dimensionless,
    opts = [u.dimensionless]
)

force = Units(
    si=u.N,
    imp=u.lbf,
    opts = [u.N, u.kN, u.lbf]
)

force_per_area = Units(
    si=u.N/u.m**2,
    imp=u.lbf/u.ft**2,
    opts = [u.N/u.m**2, u.kN/u.m**2, u.lbf/u.ft**2]
)

force_per_length = Units(
    si=u.N/u.m,
    imp=u.lbf/u.ft,
    opts = [u.N/u.m, u.kN/u.m, u.lbf/u.ft]
)

length = Units(
    si=u.m,
    imp=u.inch,
    opts = [u.nm, u.um, u.mm, u.cm, u.m, u.km, u.inch, u.ft, u.yd, u.mi]
)