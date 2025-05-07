import reflex as rx
from typing import Dict, Union, List
from reflex_nova import FrontendVar, TopologicalModel
import numpy as np
from collections.abc import Iterable
from .components.model import sigfig
import warnings
from .components.model.nomenclature import BaseNomenclature
from .components.model.fields import IndependentVar, DependentVar
from .components.reflex.components import input_with_units, output_with_units

from typing import get_origin, get_args, Dict

def _is_dict_of_str_and_frontendvar(obj):
    if not isinstance(obj, dict):
        return False
    key_type, value_type = get_args(Dict[str, FrontendVar])
    return all(isinstance(k, key_type) for k in obj.keys()) and \
           all(isinstance(v, value_type) for v in obj.values())

def _process_input_variables(variables) -> Dict[str, FrontendVar]:
    if _is_dict_of_str_and_frontendvar(variables):
        return variables
    elif isinstance(variables, BaseNomenclature):
        sub_variables= {}
        for name in dir(variables):
            attr = getattr(variables, name)
            if isinstance(attr, IndependentVar):
                sub_variables[name] = FrontendVar(
                    sym=attr.sym,
                    name=attr.name,
                    disp=attr.disp,
                    val=attr.value,
                    unit=attr.unit.si,
                    unit_opts=attr.unit.opts
                )
            elif isinstance(attr, DependentVar):
                sub_variables[name] = FrontendVar(
                    sym=attr.sym,
                    name=attr.name,
                    disp=attr.disp,
                    eqn=attr.eqn,
                    unit=attr.unit.si,
                    unit_opts=attr.unit.opts
                )
        return sub_variables
    else:
        raise ValueError("Invalid variables type. Must be a dictionary of str: FrontendVar or BaseNomenclature.")

class ReusableOptimizer(rx.ComponentState):
    # Class to implement a reusable optimizer similar to ReusableSolver
    pass

class TopologicalSolver(rx.ComponentState):
    variables: Dict[str, FrontendVar] = {}
    _model: TopologicalModel = None

    input_sorted: List[str] = []
    output_sorted: List[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the model, solve it, and update the variables
        self._model = TopologicalModel(self.variables)

        self._model.solve()
        self.update_variables()

    def update_variables(self):
        results = self._model.get_results()
        for name, value in results.items():
            if isinstance(value, Iterable):
                self.variables[name].val = [float(sigfig.round(str(v), sigfigs=4)) for v in np.atleast_1d(value)]
            else:
                self.variables[name].val = float(sigfig.round(str(value), sigfigs=4))

    @rx.event
    def on_value_change(self, name: str, value: str):
        variable = self.variables[name]
        try:
            float_value = float(value)
            variable.val = float_value

            self._model.update_variable(name, variable.val, variable.unit)
            self.update_variables()

            variable.is_valid = True
            variable.error_msg = ""
        except ValueError as e:
            variable.is_valid = False
            variable.error_msg = "Invalid value. Please enter a number."
            print(e)

    @rx.event
    def input_unit_change(self, name: str, unit: str):
        variable = self.variables[name]
        variable.unit = unit

        self._model.update_variable(name, variable.val, variable.unit)
        self.update_variables()

    @rx.event
    def output_unit_change(self, name: str, unit: str):
        variable = self.variables[name]
        variable.unit = unit

        self._model.convert_output_units(name, variable.unit)
        results = self._model.get_results()
        
        new_value = results[name]
        self.variables[name].val = float(sigfig.round(str(new_value), sigfigs=4))

    @classmethod
    def get_component(cls, *children, **props):
        variables = props.pop("variables", None)

        if variables is None:
            raise ValueError("Variables are required.")
        elif variables:
            state_variables = _process_input_variables(variables)
        
        cls.__fields__["variables"].default = state_variables

        cls.__fields__["input_sorted"].default = sorted(
            [k for k, v in state_variables.items() if v.eqn is None],
            key=lambda x: x.lower()
        )
        cls.__fields__["output_sorted"].default = sorted([k for k, v in state_variables.items() if v.eqn is not None], key=lambda x: x.lower())

        return rx.hstack(
            *children,
            rx.vstack(
                rx.foreach(
                    cls.input_sorted,
                    lambda name: input_with_units(
                        cls.variables[name],
                        cls.on_value_change,
                        cls.input_unit_change
                    )
                ),
            ),
            rx.vstack(
                rx.foreach(
                    cls.output_sorted,
                    lambda name: output_with_units(
                        cls.variables[name],
                        cls.output_unit_change
                    )
                ),
            ),
            **props,
        )
    
topological_solver = TopologicalSolver.create