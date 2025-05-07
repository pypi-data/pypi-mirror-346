import pint
from typing import List
from .unit import ureg, Unit

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

def unit_factory(
        default: pint.Unit,
        options: List[pint.Unit]
    ) -> Unit:

    """Creates a unit instance with the specified default and options."""
    return Unit(
        selected=format_unit(default),
        options=format_units(options)
    )

angle = unit_factory(
    default=ureg.radian,
    options=[ureg.deg, ureg.radian]
)

dimensionless = unit_factory(
    default=ureg.dless,
    options=[ureg.dless]
)

force = unit_factory(
    default=ureg.N,
    options=[ureg.N, ureg.kN, ureg.lbf]
)

length = unit_factory(
    default=ureg.m,
    options=[ureg.m, ureg.cm, ureg.mm, ureg.inch, ureg.ft]
)

mass = unit_factory(
    default=ureg.kg,
    options=[ureg.kg, ureg.g, ureg.lb]
)