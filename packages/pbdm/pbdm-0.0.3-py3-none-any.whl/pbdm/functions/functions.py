from pbdm.psymple_extension.psymple_connections import (
    PBDMFunctionalObject,
    PBDMCompositeObject,
    PortedObjectWithConnections,
)

from sympy import parse_expr, solve, symbols

from pbdm.age_structure.age_structure import AgeStructuredObject
from psymple.build import HIERARCHY_SEPARATOR

"""
class Function(PBDMFunctionalObject):
    Gathers "function", "function_name" from parameters.

    def initialise_object(self, **parameters):
        # self.add_parameters(**parameters)
        function_name = self.get_parameter("function_name", default="function")
        function = self.get_parameter("function")
        self.function_name = function_name
        assignments = [(function_name, function)]
        print(assignments)
        self.add_parameter_assignments(*assignments)
        super().initialise_object()
"""

# X = Function(name="X", k=10, Del=2, named="word")
# print(X.parameters)
# X.initialise_object(function="x**2")

class Function(PBDMFunctionalObject):
    """
    Required parameters:
        - function: str representation of the function

    Searched parameters:
        - output_name: str for the name of the function

    "function": {
        "function": ...,
        "output_name": ...,
    }
    """
    def initialise_object(self):
        function = self.get_parameter("function", search_ancestry=False)
        output_name = self.get_parameter("output_name", default="function")
        assignment = (output_name, function)
        print(assignment)
        self.add_parameter_assignments(assignment)
        super().initialise_object()

"""
F = Function(
    name="birth_rate",
    function="3*r",
    output_name="rate",
    inputs={"r": "10", "s": "2"},
)

F.initialise_object()
X = F.generate_ported_object()

print("FUNCTION TEST", X.to_data())
"""

class AgeStructuredFunction(PBDMFunctionalObject):
    """
    "function": "function_form"
    "output_name": "output_name"
    
    """
    def initialise_object(self):
        function = self.get_parameter("function", search_ancestry=False)
        output_name = self.get_parameter("output_name", "function")
        age_variable = self.get_parameter("age_structure.variable", default="A")
        index_variable = self.get_parameter("age_structure.index_varaible", default="i")
        structured_inputs = self.get_parameter("age_structured_inputs", default={})
        k = self.get_parameter("age_structure.k")
        index_function = self.get_parameter("age_structure.index_function", default="(i-0.5)*Del/k")
        parse_index_function = parse_expr(index_function).subs({"k": k})

        print(self.name, function)
        parse_function = parse_expr(function).subs(age_variable, parse_index_function)
        functions = [
            (f"{output_name}_{i}", parse_function.subs((input, f"{input}_{i}") for input in structured_inputs).subs(index_variable, i))
            for i in range(1, k + 1)
        ]
        self.add_parameter_assignments(*functions)
        super().initialise_object()
        AgeStructuredObject.initialise_object(self)

class AgeStructuredIntegral(PBDMFunctionalObject):
    """
    Integral of the form

    \int_{limits} f(y_1,...,y_m,a) da
    
    """
    def initialise_object(self):
        integrand = self.get_parameter("integrand")
        structured_inputs = self.get_parameter("age_structured_inputs", default={})
        age_variable = self.get_parameter("age_structure.variable", default="a")
        index_function = self.get_parameter("age_structure.index_function", default = "(i-0.5)*Del/k")
        index_variable = self.get_parameter("age_structure.index_variable", default="i")
        limits = self.search_for_parameter("limits", "all")
        k = self.search_for_parameter("age_structure.k")
        output_name = self.search_for_parameter("output_name", default="function", search_ancestry=False)

        parse_index_function = parse_expr(index_function).subs("k", k)
        sub_parse_integrand = parse_expr(integrand).subs(age_variable, parse_index_function)
        
        
        
        if limits == "all":
            limits = (1, k)

        limits = (limits[0], limits[1] + 1)

        integral_expr = "+".join(
            [
                str(
                    sub_parse_integrand.subs(
                        (input, f"{input}_{i}") for input in structured_inputs
                    ).subs(index_variable, i)
                )
                for i in range(*limits)
            ]
        )

        print(integral_expr)

        self.add_parameter_assignments((output_name, integral_expr))
        super().initialise_object()

        AgeStructuredObject.initialise_object(self)

class Functions(PBDMCompositeObject):
    """
    "functions": {
        "func_1": {
            "type": ...,
            "function": ...,
            "output_name": ...,
            "expose": ...,
            **data: {} (passed to function object)
        },
        "func_2": {...},
    **PO_data: {},
    }
    
    """
    def initialise_object(self):
        functions = self.get_parameter("functions")
        for function_name, function_data in functions.items():
            type = function_data.get("type", "single")
            output_name = function_data.get("output_name", "function")
            expose = True
            if type == "single":
                function_class = Function
            elif type == "age_structured":
                function_class = AgeStructuredFunction
            elif type == "age_structured_integral":
                function_class = AgeStructuredIntegral
            function_object = function_class(name=function_name, **function_data)
            self.add_children(function_object)

        
            if expose:
                if type in {"single", "age_structured_integral"}:
                    self.add_output_ports(function_name)
                    function_object.add_output_connection(output_name, {f"{self.name}.{function_name}"})
                elif type == "age_structured":
                    k = function_object.get_parameter("age_structure.k")
                    for i in range(1, k+1):
                        self.add_output_ports(f"{function_name}_{i}")
                        function_object.add_output_connection(f"{output_name}_{i}", {f"{self.name}.{function_name}_{i}"})

        super().initialise_object()


F = Functions(
    name="f",
    age_structure =  {
        "k": 3,
        "variable": "A",
        "index_function": "i/k",
    },
    functions={
        "birth": {
            "function": "2*x",
            "output_connections": {"function": {"f.death.birth"}},
        },
        "death": {
            "type": "age_structured",
            "function": "-2*birth",
            #"inputs": {"birth": "f.birth.function"},
            "output_name": "togo",
            #"inputs": {"birth": "functions.birth.function"},
            "age_structured_outputs": {"togo": {"f.repro.d"}}
        },
        "repro": {
            "type": "age_structured",
            "function": "4*A*r*d",
            "output_name": "repro_rate",
            "age_structured_inputs": {"d"},
        },
        "diap": {
            "type": "age_structured_integral",
            "integrand": "exp(-repro*r*A)",
            "age_structured_inputs": {"repro": "f.repro.repro_rate"},
            "output_name": "diap_rate",
        }
    }
)

"""

repro(A) = 4*A*r

A = (i-0.5)*Del/k

-> repro_i = 4*(i-0.5)*Del/k*r, i=1,...,k

diap = int(repro(A) dA)

-> repro_1 + repro_2 + ... + repro_k


"""

#F.compile_system_connections()
#X = F.generate_ported_object()
#print("FUNCTIONS OUTPUT", X.to_data())
            

"""
#TESTS
X = AgeStructuredFunction(
    name="X",
    **{
        "age_structure.variable": "A",
        # "age_structure.k": 5,
        "age_structure.index_function": "(i-0.5)*Del/k",
        "function": "4*A*r",
    },
)

#A = PBDMCompositeObject("A", children=[X], **{"age_structure.k": 5})

#X.initialise_object()
"""

"""

class FunctionsOLD(PBDMCompositeObject):
    
    Gathers "functions" from parameters
    

    def initialise_object(self):
        functions = self.search_for_parameter("functions", search_ancestry=False)
        children = [
            Functions(name=function_name, **function_data)
            for function_name, function_data in functions.items()
        ]
        self.add_children(*children)
        super().initialise_object()
        for child in children:
            child_function_name = child.function_name
            child_name = child.name
            self.add_output_ports(child_name)
            child.add_output_connection(
                f"{child_function_name}", {f"{self.name}.{child_name}"}
            )

class AgeStructuredFunction(Functions):
    
    - age_structure:
        - age_var_name
        - k
        - index_function
    - function

    "functions": {
        "ovip": {
            "function": "..."
            }
        }
    }

    

    def initialise_object(self):
        age_var_name = self.search_for_parameter(
            "age_structure.age_var_name", default="A"
        )
        k = self.search_for_parameter("age_structure.k")
        index_function = self.search_for_parameter(
            "age_structure.index_function", default=f"(i-1/2)*Del/{k}"
        )
        function = self.search_for_parameter("function")
        # calculations = self.search_for_parameter("calculations", default={})
        parse_function = parse_expr(function)
        parse_index_function = parse_expr(index_function)

        self.parameters.update(
            {
                "functions": {
                    f"{self.name}_{i}": parse_function.subs(
                        age_var_name, parse_index_function.subs("i", i)
                    )
                    for i in range(1, k + 1)
                }
            }
        )
        ### TODO: How to get dummy assignment??
        super().initialise_object()


B = AgeStructuredFunction(
    name="ovip_rate",
    function="a*b*(A-A_min)/(1 + c**A)",
    inputs={"a": 1.07, "b": 0.0127, "c": 1.001385, "A_min": 75},
)
"""
# x.compile_system_connections()
# p = x.generate_ported_object()
# print(p.input_ports["a"].default_value)
# comp = p.compile()
# print(comp.get_assignments())
# print(p.parameters["Del"])
# print(p.to_data())

"""
class AgeStructuredIntegralOLD(PBDMFunctionalObject):
    
    Integral between 1 or more age structured objects

    Syntax:
        - integrand: a*b*c
        - inputs: {"a": "address.a", ...}
        - limits: (i,j)

    Fetches:
        - age_structure.k
        - age_structure.index_function

    Creates:
        - function a_i*b_i*c_i + ... + a_j*b_j*c_j
        - inputs: {"a_i": "address.a_i" , ...}

    

    def initialise_object(self):
        integrand = self.search_for_parameter("integrand")
        function_objects = self.search_for_parameter("function_objects")
        limits = self.search_for_parameter("limits", "all")
        # variable = self.search_for_parameter("variable")

        k = self.search_for_parameter("age_structure.k")
        # index_function = self.search_for_parameter("age_structure.index_function")

        # parse_index_function = parse_expr(index_function)
        # inverse = solve(parse_index_function - symbols("g"), symbols("i"))
        # print(inverse)

        parse_integrand = parse_expr(integrand)

        # inputs = self.inputs.copy()
        # self.inputs.clear()
        # integral_objects = []
        # for input, address in inputs.items():
        # TODO: house this in get_relative() function
        # address_main = HIERARCHY_SEPARATOR.join(address.split(HIERARCHY_SEPARATOR)[:-1])
        # target_object = self.get_relative(address)
        # integral_objects.append(target_object)

        if limits == "all":
            limits = (1, k)
            # integral_object_k = [obj.search_for_parameter("k") for obj in integral_objects]
            # assert all(x == integral_object_k[0] for x in integral_object_k)
            # limits = (1, integral_object_k[0])

        limits = (limits[0], limits[1] + 1)

        integral_expr = "+".join(
            [
                str(
                    parse_integrand.subs(
                        (input, f"{input}_{i}") for input in function_objects
                    )
                )
                for i in range(*limits)
            ]
        )

        self.add_parameter_assignments(("integral", integral_expr))
        super().initialise_object()
        for input, address in function_objects.items():
            target_object = address.split(HIERARCHY_SEPARATOR)[-1]
            for i in range(*limits):
                self.add_input_connection(f"{input}_{i}", f"{address}_{i}")



C = AgeStructuredIntegral(
    name="C",
    function_objects={"a": "A.ovip_rate", "b": "A.mass"},
    integrand="2*r*a*b",
    inputs={"r": 2},
)

"A.dynamics.mass.M_1" or "A.functions.ovip.rate_1"

from functional_population import DDTM

D = DDTM("mass")

A = PBDMCompositeObject(name="A", children=[B, C, D], age_structure={"k": 3})

A.compile_system_connections()
p = A.generate_ported_object()
print(p.to_data())


f = Functions(
    name="k",
    functions={
        "func_1": {
            "function": "x+2+a",
            "inputs": {"x": 2},
        },
        "func_2": {
            "function": "2*a",
        },
    },
    inputs={"a": 1},
)

# f.compile_system_connections()
# f.generate_ported_object()
"""




