from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject
from pbdm.population_dynamics.variables import ODESystem
from psymple.build import HIERARCHY_SEPARATOR

from pbdm.functions.functions import Function, Functions

class Interaction(PBDMCompositeObject):
    def initialise_object(self):
        rate_data = self.get_parameter("functional_response", search_ancestry=False)
        rate_object = Function(name="functional_response", output_name="rate", **rate_data)

        consumer_address = self.get_parameter("consumer", search_ancestry=False)
        consumer_variable = self.get_parameter("consumer_variable", default="consumer")
        consumer_object = self.get_target(consumer_address)

        resource_address = self.get_parameter("resource", search_ancestry=False)
        resource_variable = self.get_parameter("resource_variable", default="resource")
        resource_object = self.get_target(resource_address)

        var_object = ODESystem(
            name="odes", 
            odes={
                consumer_variable: "rate",
                resource_variable: "-rate"
            }
        )

        self.add_children(var_object, rate_object)

        functions = self.get_parameter("functions", default={}, search_ancestry=False)
        if functions:
            functions_object = Functions(name="functions", functions=functions)
            self.add_children(functions_object)

        var_object.add_input_connection("rate", f"{self.name}.functional_response.rate")

        self.add_variable_ports(consumer_variable, resource_variable)
        self.add_variable_connection(consumer_variable, {f"odes.{consumer_variable}"})
        self.add_variable_connection(resource_variable, {f"odes.{resource_variable}"})

        super().initialise_object()       

"""
Interaction(
    resource = "address",
    consumer = "address",
    functional_response = {
        "function": "",
        "**inputs": ""
    },
    functions = {}
)
"""