import re
import reflex as rx
from .variables import FrontendVar
from reflex_mathjax import mathjax


def _format_symbol(text: str) -> str:
    """
    Replaces occurrences of 'X_sub' with 'X_{sub}' where 'X' is any string and 'sub' is any substring.
    
    Parameters:
        text (str): The input string.
    
    Returns:
        str: The formatted string with 'X_sub' replaced by 'X_{sub}'.
    """
    return re.sub(r'(\w+)_([a-zA-Z0-9]+)', r'\1_{\2}', text)

# Example usage:
# print(format_subscript("P_max, V_rms, I_peak, T_low, F_high, X_test"))


def _symbol_name(sym: str, name: str) -> rx.Component:
    # sym_string = _format_symbol(sym)
    return rx.hstack(
        mathjax(f"\({sym}\)"),
        rx.text(
            f"({name})",
        #     size="1",
        #     weight="bold",
        #     padding_top="1em",
        ),
        font_size="10pt",
        # font_family= "Arial, Helvetica, sans-serif"
    )

def _title(name: str) -> rx.Component:
    return rx.text(
        name, size="1",
        weight="bold",
        padding_top="1em",
    )

def _unit_select(var: FrontendVar, on_unit_change, disabled=False) -> rx.Component:
    return rx.select(
        var.unit_opts,
        value=var.unit,
        disabled=disabled,
        on_change=on_unit_change(var.sym),
        top="0",
        right="0",
        width="120px",
        variant="soft",
        radius="none",
        cursor="pointer",
        size="3",
        position="popper",
    )

def _input(var: FrontendVar, on_value_change, on_unit_change, disabled=False) -> rx.Component:
    return rx.tooltip(
        rx.box(
            rx.debounce_input(
                rx.input(
                    _unit_select(var, on_unit_change, disabled),
                    value=var.val,
                    disabled=disabled,
                    # NOTE: Somehow this works
                    on_change = on_value_change(var.sym),
                    outline = rx.cond(
                        var.is_valid,
                        "none",
                        "1px solid red",
                    ),
                    size="3",
                    type="number",
                    variant="soft",
                    width="100%",
                    overflow="hidden",
                    height="40px",
                ),
                debounce_timeout=1000,
                force_notify_by_enter=True,
                force_notify_on_blur=True,
            ),
            width="100%",
            padding="0em",
        ),
        content=var.error_msg,
        open=~var.is_valid,
        width="100%",
        padding="0em",
    )

def _output(var: FrontendVar, on_unit_change, disabled=False) -> rx.Component:
    return rx.box(
        rx.input(
            _unit_select(var, on_unit_change, disabled),
            value=var.val,
            disabled=True,
            # NOTE: Somehow this works
            # on_change = on_value_change(var.name),
            # outline = "none",
            size="3",
            type="number",
            variant="soft",
            width="100%",
            overflow="hidden",
            height="40px",
        ),
        width="100%",
        padding="0em",
    )


def input_with_units(var: FrontendVar, on_value_change: rx.EventHandler, on_unit_change) -> rx.Component:
    return rx.vstack(
        _symbol_name(var.disp, var.name),
        _input(var, on_value_change, on_unit_change),
        width="100%",
        max_width="20em",
        min_width="15em",
        spacing="0",
    )

def output_with_units(var: FrontendVar, on_unit_change) -> rx.Component:
    return rx.vstack(
        _symbol_name(var.disp, var.name),
        _output(var, on_unit_change),
        width="100%",
        max_width="20em",
        min_width="15em",
        spacing="0",
    )

def skeleton_output_with_units(var: FrontendVar, condition: bool, on_unit_change) -> rx.Component:
    return rx.vstack(
        _title(var.name),
        rx.skeleton(
            _output(var, on_unit_change),
            loading=~condition,
        ),
        width="100%",
        max_width="20em",
        min_width="15em",
        spacing="0",
    )

def checks(title, latex, condition) -> rx.Component:
    return rx.vstack(
        # rx.text(
        #     "Check Condition",
        #     size="1",
        #     weight="bold",
        #     padding_top="1em",
        # ),
        _title(title),
        rx.box(
            rx.hstack(
                rx.box(
                    mathjax(latex),
                    padding_left='1em',
                ),
                rx.spacer(),
                rx.box(
                    rx.cond(
                        condition,
                        rx.icon("thumbs-up"),
                        rx.icon("thumbs-down"),
                    ),
                    top="0",
                    right="0",
                    width="120px",
                    variant="soft",
                    radius="none",
                    padding_left="1em",
                    # margin='auto',
                ),
                align="center",
                height='100%',
            ),
            height='40px',
            width='100%',
            # padding='0.5em',
            background=rx.cond(
                condition,
                rx.color('green', 6),
                rx.color('red', 6),
            ),
            border_radius='6px',
        ),
        width='100%',
        max_width='20em',
        min_width='15em',
        spacing='0',
    )