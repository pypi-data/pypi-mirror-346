from pbdm.psymple_extension.psymple_connections import (
    PBDMFunctionalObject,
    PBDMCompositeObject,
)

from pbdm.psymple_extension.draw_ported_objects import psympleGraph

#from pbdm.abstract.rate_objects import ScalarFunctionalRates, ScalarODERates
from pbdm.abstract.function_objects import ObjectWithFunctions

from pbdm.functions.functions import Function, Functions, AgeStructuredFunction

from pbdm.population_dynamics.variables import ODESystem, DifferentialEquations

class PopulationProcess(PBDMCompositeObject):
    """
    "process_name": {
        "rate": <function data>,
        OR
        "rates": <functions data>,
        "variable": <ODE data> + "apply_scalars"
        OR
        "variables": <ODE System data> + "apply_scalars"
        "output": <> + "apply_scalars"
        OR
        "outputs": <> + "apply_scalars"
        "functions": <>
    }
    """

    def initialise_object(self):
        action_objects = []
        rates = self.get_parameter("rates", search_ancestry=False)
        rates_object = Functions(name="rates", functions=rates)
        self.add_children(rates_object)

        variables = self.get_parameter("variables", default={}, search_ancestry=False)
        if variables:
            variables_object = DifferentialEquations("variables", odes=variables)
            action_objects.append(variables_object)

        outputs = self.get_parameter("outputs", default = {}, search_ancestry=False)
        if outputs:
            outputs_object = Functions("outputs", functions=outputs)
            action_objects.append(outputs_object)

        functions = self.get_parameter("functions", default={}, search_ancestry=False)
        if functions:
            functions_object = Functions("functions", functions=functions)
            self.add_children(functions_object)

        self.add_children(*action_objects)

        super().initialise_object()

        for action_object in action_objects:
            for object in action_object.children.values():
                print("HERE", rates_object.output_ports, object.name, object.input_ports)
                for output in set(rates_object.output_ports).intersection(set(object.input_ports)):
                    #print("HERE", output)
                    object.add_input_connection(output, f"{self.name}.rates.{output}", overwrite=False)
            action_object.expose_outputs(self)
            action_object.expose_variables(self)

        action_objects.append(rates_object)

        if functions:
            for child_object in action_objects:
                for object in child_object.children.values():
                    for function in set(functions_object.output_ports).intersection(set(object.input_ports)):
                        object.add_input_connection(function, f"{self.name}.functions.{function}", overwrite=False)


class BasicPopulationProcess(PopulationProcess):
    """
    "process": {
        "rate": str
        "age_structured": bool
        "demand_based": bool

    }
    
    """
    def initialise_object(self):
        rate = self.get_parameter("rate", search_ancestry=False)
        age_structured = self.get_parameter("age_structured", search_ancestry=False, default=False)
        demand_based = self.get_parameter("demand_based", search_ancestry=False, default=False)
        impl_type = "age_structured" if age_structured else "single"
        
        rate_data = {
            "rate": {
                "type": impl_type,
                "function": rate,
            }
        }

        variable_data = {
            "variable": {
                "type": impl_type,
                "function": "rate*SD" if demand_based else "rate",
                "age_structured_inputs": {"rate"} if age_structured else {}
            }
        }

        print(variable_data, type(variable_data))

        self.add_parameters(rates=rate_data, variables=variable_data)

        if demand_based:
            outputs_data = {
                "demand": {
                    "type": impl_type,
                    "function": "rate",
                    "age_structured_inputs": {"rate"} if age_structured else {},
                },
            }
            if age_structured: 
                outputs_data |= {
                    "total_demand": {
                        "type": "age_structured_integral",
                        "integrand": "rate",
                        "age_structured_inputs": {"rate"}
                    }
                }

            self.add_parameters(outputs=outputs_data)


        super().initialise_object()


#P.compile_system_connections()
#X = P.generate_ported_object()
#print(X.to_data())

"""
PS = PopulationProcess(
    name="photosynthesis",
    type="functional",
    rate={
        "function": "demand * (1 - exp(- search*potential / demand))",
        "inputs": {"search": "photosynthesis.functions.search", "potential": "photosynthesis.functions.potential"},
    },
    variable="PS",
    scalars={"SD_veg": 0.5},
    functions={
        "LAI": {
            "function": "4*M",
        },
        "potential": {
            "function": "solar_rad / a * conv",
            "inputs": {"a": 3.875, "conv": 0.0929}
        },
        "search": {
            "function": "1 - exp(-rd*LAI)",
            "inputs": {"rd": 0.89, "LAI": "functions.LAI.function"}
        }
    }
)
"""
#PS.compile_system_connections()
#X = PS.generate_ported_object()

M = PopulationProcess(
    name="mortality",
    rates={
        "frost_mortality": {"type": "age_structured", "function": "4*sqrt(T)"},
        "density_mortality": {"function": "2*r*s", "inputs": {"r": 10}},
    },
    age_structure={"k": 3},
    variable="M",
    variables={
        "x": { 
            "function": "density_mortality*mass_factor*SD_water",
        },
        "y": {
            "type": "age_structured",
            "variable": "n",
            "function": "frost_mortality*SD_water",
            "age_structured_inputs": {"frost_mortality"},
        },
        "v": {
            "function": "density_mortality*SD_food",
        },
    },
    functions={
        "SD_water": {
            "function": "a*T",
            "inputs": {"a": 0.73}
        }
    },
    input_ports=[("SD_food", 0.3)],
)

growth_pred = PopulationProcess(
    name="growth",
    a = 4,
    age_structure = {"k": 3},
    rates = {
        "grow_opt": {
            "type": "age_structured",
            "function": "a*M",
            "inputs": {"M": "growth.functions.mass"}
        }
    },
    variables = {
        "M": {
            "type": "age_structured",
            "variable": "M",
            "function": "grow_opt*SD_food",
            "age_structured_inputs": {"grow_opt"},
        }
    },
    outputs = {
        "demand_total": {
            "type": "age_structured_integral",
            "integrand": "grow_opt",
            "output_name": "function",
            "age_structured_inputs": {"grow_opt"},
        },
        "demand": {
            "type": "age_structured",
            "function": "grow_opt",
            "age_structured_inputs": {"grow_opt"},
        }
    },
    functions = {
        "mass": {
            "function": "2*sin(T)",
        }
    }
)

# TODO: Bug if {"supply": "??.rates.response"}

int = PopulationProcess(
    name="interaction",
    age_structure = {"k": 3},
    rates={
        "response": {
            "type": "age_structured",
            "function": "- (1-exp(-D))",
            "inputs": {"D": "interaction.functions.total_demand"},
        },
        "SD_ratio": {
            "function": "supply/demand",
            "inputs": {"supply": "interaction.functions.integrate_response", "demand": "interaction.functions.total_demand"},
        }
    },
    variables={
        "prey_n": {
            "type": "age_structured",
            "function": "response",
            "age_structured_inputs": {"response"},
        },
    },
    functions={
        "total_demand": {
            "type": "age_structured_integral",
            "integrand": "D",
            "age_structured_inputs": {"D": "system.growth.demand"},
        },
        "integrate_response": {
            "type": "age_structured_integral",
            "integrand": "supply",
            #"age_structured_inputs": {"supply": "interaction.rates.response"}
        }
    }

)

system = PBDMCompositeObject(
    name="system",
    children=[int, growth_pred],
)



basic = BasicPopulationProcess(
    name="growth",
    age_structure={"k": 3},
    age_structured=True,
    demand_based=True,
    rate="a*(1-exp(-b))",
    variable="M"
)

#basic.compile_system_connections()
#X = basic.generate_ported_object()
#data = X.to_data()
#print(data)
"""
G = psympleGraph(data)
A = G.to_pgv()

A.layout(prog="dot", args="-Efontsize=8")
A.draw("file.svg")
"""







