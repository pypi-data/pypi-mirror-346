import reflex as rx
import pint

from typing import List, Optional
# from .units import format_unit, format_units

ureg = pint.UnitRegistry()
ureg.define("dless = 1 = Ø")

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
    ) -> 'Unit':

    """Creates a unit instance with the specified default and options."""
    return Unit(
        selected=format_unit(default),
        options=format_units(options)
    )

def _in_same_system(u1: str, u2: str) -> bool:
    """
    Return True if both unit names u1 and u2 live in the same
    measurement system (SI or Imperial/US).
    """
    # grab the attribute names under each system namespace
    si_units  = set(dir(ureg.sys.SI))
    imp_units = set(dir(ureg.sys.imperial)) | set(dir(ureg.sys.US))

    in_si_1  = u1  in si_units
    in_imp_1 = u1  in imp_units
    in_si_2  = u2  in si_units
    in_imp_2 = u2  in imp_units

    # only allow if both in SI or both in Imperial
    return (in_si_1 and in_si_2) or (in_imp_1 and in_imp_2)

def _join(a: str, b: str) -> str:
    """Alphabetically (case-insensitive) join two unit names with '·'."""
    return f"{a}·{b}" if a.lower() < b.lower() else f"{b}·{a}"

class Unit(rx.Base):
    """A class representing a unit with a value and options."""
    selected: Optional[str]
    options: Optional[list[str]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __mul__(self, other: 'Unit') -> 'Unit':
        if not isinstance(other, Unit):
            return NotImplemented

        # parse the two selected units
        u_self  = ureg.parse_units(self.selected)
        u_other = ureg.parse_units(other.selected)

        # multiply for the "selected" display
        prod    = u_self * u_other
        new_selected = format_unit(prod)

        new_opts = []
        # if they’re the same physical dimension, just square each option
        if u_self.dimensionality == u_other.dimensionality:
            for opt in (self.options or []):
                u_opt = ureg.parse_units(opt)
                new_opts.append(format_unit(u_opt ** 2))
        else:
            # different dimensions → do full cross‐product
            for opt1 in (self.options or []):
                for opt2 in (other.options or []):
                    u1 = ureg.parse_units(opt1)
                    u2 = ureg.parse_units(opt2)
                    new_opts.append(format_unit(u1 * u2))

        # de-duplicate & sort
        new_opts = sorted(set(new_opts))

        return Unit(selected=new_selected, options=new_opts)


    def __repr__(self) -> str:
        return f"Unit(selected={self.selected!r}, options={self.options!r})"
    
    def __str__(self) -> str:
        return self.selected

    def __eq__(self, other) -> bool:
        if isinstance(other, Unit):
            return self.selected == other.selected
        elif isinstance(other, str):
            return self.selected == other
        return False

    def update_selected(self, new_unit: str) -> 'Unit':
        """Update the selected unit, ensuring it's a valid option."""
        if new_unit in self.options:
            return Unit(selected=new_unit, options=self.options)
        else:
            raise ValueError(f"'{new_unit}' is not a valid option. Valid options: {self.options}")