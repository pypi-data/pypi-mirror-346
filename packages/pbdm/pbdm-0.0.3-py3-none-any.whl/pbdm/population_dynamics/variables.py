from pbdm.psymple_extension.psymple_connections import (
    PBDMFunctionalObject,
    PBDMCompositeObject,
    PBDMVariableObject,
    PortedObjectWithConnections,
)

from pbdm.psymple_extension.draw_ported_objects import psympleGraph

from pbdm.age_structure.age_structure import AgeStructuredObject

from sympy import parse_expr, solve, symbols

from psymple.build import HIERARCHY_SEPARATOR


class ODESystem(PBDMVariableObject, AgeStructuredObject):
    def initialise_object(self):
        odes = self.get_parameter("odes", search_ancestry=False)
        assignments = list(odes.items())
        self.add_variable_assignments(*assignments)
        super().initialise_object()
        try:
            self.get_parameter("age_structure.k")
            AgeStructuredObject.initialise_object(self)
        except:
            pass

        self.odes = odes

    """
    def expose(self, object, variables=None):
        if object not in self.parents.values():
            raise Exception(f"Cannot expose ports from {self.name} to {object.name} because {object.name} is not an ancestor.")
        if (not variables) or (variables is True):
            variables = {variable: variable for variable in self.odes}
        object.add_variable_ports(*variables.values())
        for variable, expose_name in variables.items():
            self.add_variable_connection(variable, {f"{object.name}.{expose_name}"})
    """

class ODE(ODESystem):
    def initialise_object(self):
        
        function = self.get_parameter("function", search_ancestry=False)
        variable = self.get_parameter("variable", default="var")
        print("ODES", self.address, function, variable)
        ode = {variable: function}
        self.add_parameters(odes=ode)
        super().initialise_object()


class AgeStructuredODESystem(ODESystem, AgeStructuredObject):
    """
    "system": {
        "age_structure": {
            "k",
            "index_function",
            "variable",
        }
        "function":
        "variable":
    }

    """

    def initialise_object(self):
        function = self.get_parameter("function", search_ancestry=False)
        variable = self.get_parameter("variable", "var")
        age_variable = self.get_parameter("age_structure.variable", default="A")
        index_variable = self.get_parameter("age_structure.index_variable", default="i")
        k = self.get_parameter("age_structure.k")
        structured_inputs = self.get_parameter("age_structured_inputs", default={})
        print(structured_inputs)
        
        index_function = self.get_parameter(
            "age_structure.index_function", "(i-0.5)*Del/k"
        )
        parse_index_function = parse_expr(index_function).subs({"k": k})
        parse_function = parse_expr(function).subs(
            [
                (age_variable, parse_index_function),
                (variable, "+".join([f"{variable}_{i}" for i in range(1, k + 1)])),
            ]
        )
        odes = {
            f"{variable}_{i}": parse_function.subs(index_variable, i).subs([(input, f"{input}_{i}") for input in structured_inputs])
            for i in range(1, k + 1)
        }
        print(odes)
        self.add_parameters(odes=odes)
        super().initialise_object()
        AgeStructuredObject.initialise_object(self)


class PopulationVariable(ODESystem):
    def initialise_object(self):
        variable_name = self.get_parameter("variable", default=self.name)
        odes = {variable_name: 0}

        stage_structure = self.get_parameter("stage_structure", default={})
        print("STAGED1", stage_structure)
        if stage_structure:
            next_stage = stage_structure.get("next_stage", {})
            ancestor = stage_structure.get("ancestor", {})
            print("STAGED", next_stage, self.parent.parent.name)
            assert isinstance(next_stage, dict)
            split_functions = []
            inputs = {}
            for stage, split_function in next_stage.items():
                print(stage, split_function)
                func = split_function.get("rate", 1)
                ode_data = {
                    f"{variable_name}_out_{stage}": f"{variable_name}*{func}",
                }
                odes.update(ode_data)
                split_functions.append(func)
                inputs |= split_function.get("inputs", {})
                target_variable = split_function.get("target_variable", variable_name)
                target_address = (
                f"{ancestor}.{stage}.dynamics.{self.name}.{target_variable}"
                )
                self.add_variable_connection(f"{variable_name}_out_{stage}", {target_address})
            decr_rate = "+".join(split_functions)
            odes[variable_name] = f"-({decr_rate})*{variable_name}"

        print("ODEINP", odes, inputs)
        self.add_parameters(odes=odes)
        super().initialise_object()
        for port, input in inputs.items():
            self.add_input_connection(port, input)                            
        



ODE_TYPES = {
    "single": ODE,
    "system": ODESystem,
    "age_structured": AgeStructuredODESystem,
}


class DifferentialEquations(PBDMCompositeObject):
    """
    "odes": {
        "ode_1": {
            "type": "ode",
            "expose": <expose>,
            "variable": <variable_name>,
            "function": <function>
            **data
        },
        "system_1": {
            "type": "system",
            "expose": <expose>,
            "variable": <??>
            "odes": {
                "var_1": <function_1>,
                "var_2": <function_2>,
                "var_3": {...},
            },
            **data:
        },
        "as_ode_1": {
            "type": "age_structured",
            "age_structure": {},
            "expose": <expose>,
            "variable": <variable>,
            "function": <function>,
            **data
        }
        "system_2": {...} (ODESystem),
    **PO_data: {},
    }
    """

    def initialise_object(self):
        odes_data = self.get_parameter("odes", search_ancestry=False)
        for name, data in odes_data.items():
            type = data.pop("type", "single")
            ODEClass = ODE_TYPES.get(type)
            ode_object = ODEClass(name=name, **data)
            self.add_children(ode_object)

        super().initialise_object()

        #print(self.name, odes_data)
        for name, data in odes_data.items():
            expose = data.pop("expose", {})
            ode_object = self.children.get(name)
            ode_object.expose_variables(self, expose)
        
    """            
    def expose(self, object):
        for child in self.children.values():
            child.expose(object)
    """

D = DifferentialEquations(
    name="des",
    age_structure={
        "variable": "a",
    },
    r=10,
    odes={
        "ode_1": {
            "function": "4*r*x",
            "variable": "x",
            "expose": {"x": "v"},
        },
        "system_1": {
            "type": "system",
            "variable": "x",
            "odes": {
                "x_1": "4*x_1*x_2*r",
                "x_2": "2*s - r*x_1",
            },
            #"expose": {"x_1": "x", "x_2": "y"},
            "s": 10,
        },
        "as_ode_1": {
            "type": "age_structured",
            "age_structure": {"k": 3},
            "function": "4*a*y**2*r",
            "variable": "y",
            "inputs": {"r": 3},
            "variable_connections": {"y_2": {"des.system_1.x_2"}},
            "expose": {"y_1": "d_1"}
        },
    },
)

"""
D.compile_system_connections()
X = D.generate_ported_object()
data = X.to_data()

G = psympleGraph(data)
A = G.to_pgv()

A.layout(prog="dot", args="-Efontsize=8")
A.draw("file.pdf")

print(data)
"""

"""
X = PBDMFunctionalObject("X", assignments=[("x", "3*r*y")])
print([asg.parameter.name for asg in X.assignments.values()])
X = X.generate_ported_object()
print(X.to_data())
"""