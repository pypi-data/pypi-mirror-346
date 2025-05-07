import numpy as np
import sympy as sp
from typing import Callable, Optional, Union, List, Dict, Set, Tuple, Any
from ..components.model.variables import ModelVar
from reflex_nova.components.reflex.variables import FrontendVar
from reflex_nova.components.model.units import Q_, u
import inspect
from ..components.model.modules import modules

from .parsing import parse_equation, parse_piecewise_equation

class TopologicalModel:
    """
    A model engine that registers variables, manages dependencies, and computes
    dependent variable values in the correct order.
    """
    def __init__(self, variables: Dict[str, FrontendVar]) -> None:
        self._variables: Dict[str, ModelVar] = self._init_model_variables(variables)
        self._dependency_graph: Dict[str, Set[str]] = self._build_dependency_graph()
        self._topological_order: List[str] = self._topological_sort()

    def _init_model_variables(self, variables: Dict[str, FrontendVar]) -> Dict[str, ModelVar]:
        """
        Initialize model variables from FrontendVar definitions.
        
        For independent variables (with no equation), their value and unit are set.
        For dependent variables (with an equation), the equation is parsed and a
        corresponding computation function is created.
        """
        model_vars: Dict[str, ModelVar] = {}
        for name, var in variables.items():
            if var.eqn is None:
                model_vars[name] = ModelVar(
                    sym=name,
                    val=var.val,
                    unit=var.unit,
                    qty=Q_(var.val, var.unit),
                )
            elif isinstance(var.eqn, str):
                deps, eq_func, eq_tex = parse_equation(var.eqn)
                model_vars[name] = ModelVar(
                    sym=name,
                    eqn=var.eqn,
                    unit=var.unit,
                    deps=deps,
                    eq_func=eq_func,
                    eq_tex=eq_tex,
                )
            elif isinstance(var.eqn, list):
                deps, eq_func, eq_tex = parse_piecewise_equation(var.eqn)
                model_vars[name] = ModelVar(
                    sym=name,
                    eqn=var.eqn,
                    unit=var.unit,
                    deps=deps,
                    eq_func=eq_func,
                    eq_tex=eq_tex,
                )
            else:
                raise ValueError(f"Invalid equation type for variable '{name}'.")
        return model_vars

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """
        Build a dependency graph mapping each variable name to the set of variable names it depends on.
        """
        graph: Dict[str, Set[str]] = {}
        for name, mv in self._variables.items():
            graph[name] = set(mv.deps) if mv.eq_func is not None else set()
        return graph

    def _topological_sort(self) -> List[str]:
        """
        Compute a topological ordering of variables based on their dependencies.
        
        Returns:
            A list of variable names in the order they should be computed.
        
        Raises:
            Exception: If a circular dependency is detected.
        """
        # Make a copy of the dependency graph
        graph = {node: set(deps) for node, deps in self._dependency_graph.items()}
        sorted_order: List[str] = []
        no_deps = {node for node, deps in graph.items() if not deps}

        while no_deps:
            node = no_deps.pop()
            sorted_order.append(node)
            for other_node in graph:
                if node in graph[other_node]:
                    graph[other_node].remove(node)
                    if not graph[other_node]:
                        no_deps.add(other_node)

        if any(graph[node] for node in graph):
            raise Exception("Circular dependency detected!")
        return sorted_order

    def solve(self) -> None:
        """
        Compute values for all dependent variables following the topological order.
        """
        for var_name in self._topological_order:
            mv = self._variables[var_name]
            if mv.eq_func is None:
                continue  # Skip independent variables.
                # Build context using the magnitude of each dependency.
            context: Dict[str, Any] = {}
            for dep in mv.deps:
                if dep not in self._variables:
                    raise ValueError(f"Dependency '{dep}' not found for variable '{mv.sym}'.")
                dep_quantity = self._variables[dep].qty
                if dep_quantity is None:
                    raise ValueError(f"Dependency '{dep}' for variable '{mv.sym}' has no value.")
                context[dep] = dep_quantity
                # print(mv.sym, context)
            try:
                result = mv.eq_func(**context)
            except Exception as e:
                raise Exception(f"Error computing variable '{mv.sym}': {e}") from e

            # Wrap the result as a Pint Quantity if a unit is provided.
            if isinstance(result, Q_):
                result_qty = result.to(mv.unit)
            else:
                result_qty = Q_(result, mv.unit)
            mv.qty = result_qty
            if isinstance(result_qty.magnitude, np.ndarray):
                mv.val = np.atleast_1d(result_qty.magnitude)
            else:
                mv.val = result_qty.magnitude

    def reset_computed(self) -> None:
        """
        Reset computed values for all dependent variables.
        """
        for mv in self._variables.values():
            if mv.eq_func is not None:
                mv.val = None
                mv.qty = None

    def update_variable(
        self,
        name: str,
        new_value: Union[float, np.ndarray, Q_],
        unit: Optional[str] = None
    ) -> None:
        """
        Update the value of an independent variable and recompute dependent variables.

        Parameters:
            name: The variable name to update.
            new_value: The new value (scalar, numpy array, or Q_).
            unit: The unit of the new value if it is not already a Q_.
        
        Raises:
            KeyError: If the variable is not found.
            ValueError: If a non-Quantity value is provided without a unit.
        """
        if name not in self._variables:
            raise KeyError(f"Variable '{name}' not found!")
        mv = self._variables[name]
        if isinstance(new_value, Q_):
            mv.qty = new_value
            mv.val = new_value.magnitude
        else:
            if unit is None:
                raise ValueError("A unit must be provided for non-Quantity values.")
            mv.qty = Q_(new_value, unit)
            mv.val = new_value
        self.reset_computed()
        self.solve()

    def convert_output_units(self, name: str, new_unit: str) -> None:
        """
        Convert the unit of a variable's value.

        Parameters:
            name: The variable name whose unit should be converted.
            new_unit: The target unit as a string.
        
        Raises:
            KeyError: If the variable is not found.
            ValueError: If the variable has no computed value.
        """
        if name not in self._variables:
            raise KeyError(f"Variable '{name}' not found!")
        mv = self._variables[name]
        if mv.qty is None:
            raise ValueError(f"Variable '{name}' has no value to convert.")
        mv.qty = mv.qty.to(new_unit)
        mv.val = mv.qty.magnitude
        mv.unit = new_unit
        # Note: Converting output units does not require recomputation.

    def get_results(self) -> Dict[str, float]:
        """
        Retrieve computed values for all variables.

        Returns:
            A dictionary mapping variable names to their computed numeric values.
        """
        return {name: mv.val for name, mv in self._variables.items()}
