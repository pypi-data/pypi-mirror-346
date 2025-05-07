import re
from typing import Union
from .fields import IndependentVar, DependentVar

def format_subscript(text: str) -> str:
    """
    Replaces occurrences like 'X_sub1_sub2' with 'X_{sub1, sub2}'.

    Parameters:
        text (str): The input string.

    Returns:
        str: The formatted string.
    """
    def repl(match):
        base = match.group(1)
        subs = match.group(2)  # This contains one or more '_sub' parts, e.g. "_sub1_sub2"
        # Split the subscripts on '_' and remove empty strings.
        parts = [p for p in subs.split('_') if p]
        # Join the parts with ', ' and wrap them in a single set of braces.
        return f"{base}_{{{', '.join(parts)}}}"
    
    # Use [^_]+ for the base (characters until the first underscore)
    return re.sub(r'([^_]+)((?:_[a-zA-Z0-9]+)+)', repl, text)


def replace_symbol(text: str) -> str:
    """
    Replaces occurrences of 'eta' with '\\eta' and 'rho' with '\\rho' in the input string.

    Parameters:
        text (str): The original string.

    Returns:
        str: The modified string with the replacements.
    """
    # Replace "eta" with "\eta"
    text = text.replace("eta", "\\eta")
    # Replace "rho" with "\rho"
    text = text.replace("rho", "\\rho")
    return text


class BaseNomenclature:
    def __init__(self):
        self._format_equations()
        
    def _format_equations(self):
        # Build a mapping from attribute name to its symbol
        symbol_mapping = {
            name: getattr(self, name).sym
            for name in dir(self)
            if not name.startswith("_") and isinstance(getattr(self, name), Union[IndependentVar, DependentVar])
        }
        # print(symbol_mapping)
        # Update each NamespaceAttr that has an eqn template with the actual symbols
        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, DependentVar) and attr.eqn:
                attr.disp = format_subscript(attr.disp)
                # Replace symbols in the equation string
                attr.disp = replace_symbol(attr.disp)
                try:
                    if isinstance(attr.eqn, list):
                        attr.eqn = [(eqn.format(**symbol_mapping) for eqn in eqn_tuple) for eqn_tuple in attr.eqn]
                    elif isinstance(attr.eqn, str):
                        attr.eqn = attr.eqn.format(**symbol_mapping)
                    else:
                        raise ValueError(f"Invalid eqn type for {name}: {attr.eqn}")
                except KeyError as e:
                    raise KeyError(f"Missing symbol in equation for {name}: {e}")
            elif isinstance(attr, IndependentVar):
                attr.disp = format_subscript(attr.disp)
                # Replace symbols in the equation string
                attr.disp = replace_symbol(attr.disp)