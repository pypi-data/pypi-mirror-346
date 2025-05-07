from pbdm.psymple_extension.psymple_connections import (
    PBDMCompositeObject,
    PBDMFunctionalObject,
    PBDMVariableObject,
)
from pbdm.functions.functions import Function, Functions
from pbdm.population_dynamics.variables import DifferentialEquations


 


class ScalarFunctionalRates(PBDMCompositeObject):
    """
    "rates": { (Functions object)
        "rate_1": {
            "function": ...,
            "inputs": ...
        },
        "rate_2": {...},
    },
    "outputs": {
        "out_1": {
            "rate": <rate from rates>,
            "scalars": {
                "scalar_1": <input or address>,
                "scalar_2": ...,
            }
        }
    },
    **PO_data: {...}
    """

    def initialise_object(self):
        rates_data = self.get_parameter("rates", search_ancestry=False)

        rates_object = Functions(name="rates", functions=rates_data)
        self.add_children(rates_object)

        outputs_data = self.get_parameter("outputs", default={}, search_ancestry=False)
        if outputs_data:
            output_functions = {
                output_name: {
                    "function": "*".join(
                        list(scalars := output_data.get("scalars", {}))
                        + [rate_name := output_data.get("rate")]
                    ),
                    "inputs": scalars | {rate_name: f"{self.name}.rates.{rate_name}"},
                }
                for output_name, output_data in outputs_data.items()
            }
            outputs_object = Functions(name="outputs", functions=output_functions)
            self.add_children(outputs_object)

        if outputs_data:
            for output_name in outputs_data:
                self.add_output_ports(output_name)
                outputs_object.add_output_connection(
                    output_name, {f"{self.name}.{output_name}"}
                )
        else:
            for rate_name in rates_data:
                self.add_output_ports(rate_name)
                rates_object.add_output_connection(
                    rate_name, {f"{self.name}.{rate_name}"}
                )

        super().initialise_object()


S = ScalarFunctionalRates(
    name="scalar_rates",
    rates={
        "frost_mortality": {"function": "4*sqrt(T)"},
        "density_mortality": {"function": "2*r*s", "inputs": {"r": 10}},
    },
    outputs={
        "mass_frost_mortality": {
            "rate": "frost_mortality",
            "scalars": {
                "mass_scale_factor": 0.001,
                "SD_water": "scalar_rates.SD_water",
            },
        },
        "number_frost_mortaity": {
            "rate": "frost_mortality",
            "scalars": {"SD_water": "scalar_rates.SD_water"},
        },
        "density_mortality": {
            "rate": "density_mortality",
            "scalars": {"SD_food": "scalar_rates.SD_food"},
        },
    },
    input_ports=[("SD_water", 0.5), ("SD_food", 0.3)],
)

#S.compile_system_connections()
#X = S.generate_ported_object()

from pbdm.psymple_extension.draw_ported_objects import psympleGraph




class ScalarODERates(PBDMCompositeObject):
    """
    "rates": { (Functions object)
        "rate_1": {
            "type": ...,
            "function": ...,
            "inputs": ...
        },
        "rate_2": {...},
    },
    "variables": { (DifferentialEquations Object)
        "var_1": {
            "type": <single or age_structured = single>
            "rate": <rate from rates>,
            "scalars": {
                "scalar_1": <input or address>,
                "scalar_2": ...,
            }
        }
    },
    **PO_data: {...}
    """

    def initialise_object(self):
        rates_data = self.get_parameter("rates", search_ancestry=False)

        rates_object = Functions(name="rates", functions=rates_data)
        self.add_children(rates_object)

        ode_data = self.get_parameter("variables", search_ancestry=False)
        ode_functions = {}
        vars = []
        for variable_name, variable_data in ode_data.items():
            type = variable_data.pop("type", "ode")
            scalars = variable_data.pop("scalars", {})
            rate_name = variable_data.pop("rate")
            if type == "ode":
                inputs = scalars | {rate_name: f"{self.name}.rates.{rate_name}"}
                function = "*".join(
                    list(scalars) + [rate_name]
                )
                data = {
                    "type": type,
                    "function": function,
                    "variable": variable_name,
                    "inputs": inputs,
                } | variable_data
            elif type == "age_structured":
                k = self.get_parameter("age_structure.k")
                inputs = scalars | {f"{rate_name}_{i}": f"{self.name}.rates.{rate_name}_{i}" for i in range(1,k+1)}
                data = {
                    "type": "system",
                    "odes": {
                        f"{variable_name}_{i}": "*".join(list(scalars) + [f"{rate_name}_{i}"])
                        for i in range(1, k+1) 
                    },
                    "inputs": inputs,
                } | variable_data
            
            

            ode_functions.update({f"system_{variable_name}": data})

        # else:
        #    ode_functions = {
        #        rate_name: {
        #            "function": "rate_function",
        #            "inputs": {"rate_function": f"{self.name}.rates.{rate_name}"}
        #        }
        #        for rate_name in rates_data
        #    }
        odes_object = DifferentialEquations(name="variables", odes=ode_functions)
        self.add_children(odes_object)
        
        vars = odes_object.variable_ports
        self.odes = vars
        super().initialise_object()
        for var_name in vars:
            print(self.input_ports, self.variable_ports)
            print("adding var port", var_name, self.name)
            self.add_variable_ports(var_name)
            print(f"adding variable connection in {odes_object.name} from {var_name} to {self.name}.{var_name}")
            odes_object.add_variable_connection(var_name, {f"{self.name}.{var_name}"})
            # This might be janky?
            #rates_object.add_input_ports(var_name)
            #rates_object.add_input_connection(var_name, f"{self.name}.vars.{var_name}")

        

    def expose(self, object):
        for var_name in self.odes:
            object.add_variable_ports(var_name)
            self.add_variable_connection(var_name, {f"{object.address}.{var_name}"})


S = ScalarODERates(
    name="scalar_rates",
    age_structure={"k": 3},
    rates={
        "frost_mortality": {
            "type": "age_structured",
            "function": "4*sqrt(T)*x*A", 
            "inputs": {"x": "scalar_rates.variables.x_1"},
        },
        "density_mortality": {"function": "2*r*s*x", "inputs": {"r": 10, "x": "scalar_rates.variables.x_1"}},
    },
    variables={
        "x": {"type": "age_structured", "rate": "frost_mortality", "scalars": {"SD_water": "scalar_rates.SD_water"}},
        "y": {"rate": "density_mortality", "scalars": {"SD_water": "scalar_rates.SD_water", "SD_food": "scalar_rates.SD_food"}},
    },
    input_ports=[("SD_water", 0.5), ("SD_food", 0.3)],
)


# def recur_cons(obj, attr):
#    print(obj.name, obj.__getattribute__(attr))
#    for child in obj.children.values():
#        recur_cons(child, attr)


S.compile_system_connections()
X = S.generate_ported_object()
print(X.to_data())
"""
G = psympleGraph(X.to_data())
A = G.to_pgv()

A.layout(prog="dot", args="-Efontsize=8")
A.draw("file.svg")
"""