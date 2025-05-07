class AgeStructuredObject:
    def initialise_object(self):
        k = self.get_parameter("age_structure.k")
        structured_inputs = self.get_parameter("age_structured_inputs", {})
        if isinstance(structured_inputs, (set, list)):
            structured_inputs = {}
        structured_outputs = self.get_parameter("age_structured_outputs", {})
        if isinstance(structured_outputs, set):
            structured_outputs = {}
        structured_variables = self.get_parameter("age_structured_variables", {})
        if isinstance(structured_variables, set):
            structured_variables = {}
        for port, address in structured_inputs.items():
            for i in range(1, k+1):
                self.add_input_connection(f"{port}_{i}", f"{address}_{i}")
        for port, destinations in structured_outputs.items():
            for i in range(1, k+1):
                new_destinations = {f"{destination}_{i}" for destination in destinations}
                self.add_output_connection(f"{port}_{i}", new_destinations)
                print("adding", port, destinations)
        for port, destinations in structured_variables.items():
            for i in range(1, k+1):
                new_destinations = {f"{destination}_{i}" for destination in destinations}
                self.add_variable_connection(f"{port}_{i}", new_destinations)


from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject, PBDMFunctionalObject

from sympy import parse_expr

class AgeStructuredFunction(PBDMFunctionalObject, AgeStructuredObject):
    def initialise_object(self):
        function = self.get_parameter("function")
        output_name = self.get_parameter("output_name", default="function")
        age_structured_inputs = self.get_parameter("age_structured_inputs", default={})
        parse_function = parse_expr(function)
        k = self.get_parameter("age_structure.k")
        assignments = {
            f"{output_name}_{i}": parse_function.subs([(input, f"{input}_{i}") for input in age_structured_inputs])
            for i in range(1,k+1)
        }

        self.add_parameter_assignments(*assignments.items())

        print(assignments)
        
        super().initialise_object()
        AgeStructuredObject.initialise_object(self)

A = AgeStructuredFunction(name="as_fun", function="5*a*rate*grey", age_structured_inputs={"rate": "system.as_rate.function"}, inputs={"grey": "system.func.function"})
B = AgeStructuredFunction(name="as_rate", function="3*a*b*c", age_structured_inputs={"c"})
D = AgeStructuredFunction(name="as_run", function="2", age_structured_outputs={"function": {"system.as_rate.c"}})
C = PBDMFunctionalObject(name="func", assignments=[("function", "3*b")])

S = PBDMCompositeObject(name="system", age_structure={"k": 5}, children=[A,B,C,D])
"""
S.compile_system_connections()
X = S.generate_ported_object()
data = X.to_data()
print(data)
"""