from pbdm.functions.functions import Function, Functions
from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject


class DemandAggregation(Functions):
    def initialise_object(self):
        components = self.get_parameter("demand")

        functions = {
            component: {
                "function": "+".join([f"D_{input}" for input in inputs]),
                "inputs": {f"D_{input}": address for input, address in inputs.items()},
            }
            for component, inputs in components.items()
        }

        self.add_parameters(functions=functions)

        super().initialise_object()


class SupplyAggregation(Function):
    def initialise_object(self):
        components = self.get_parameter("supply")

        function = "+".join(
            [
                f"S_{component}_{input}"
                for (component, inputs) in components.items()
                for input in inputs
            ]
        )
        output_name = "supply"
        function_inputs = {
            f"S_{component}_{input}": address
            for (component, inputs) in components.items()
            for (input, address) in inputs.items()
        }

        self.add_parameters(
            function=function, output_name=output_name, inputs=function_inputs
        )

        for input, address in function_inputs.items():
            self.add_input_connection(input, address)
        super().initialise_object()


class AllocationUnit(Functions):
    def initialise_object(self):
        options = self.get_parameter("options", {})
        output_name = options.get("output_name", "resource_out")
        input_name = options.get("input_name", "resource_in")
        demand_name = options.get("demand_name", "demand")
        allocate_name = options.get("allocate_name", "allocate")
        expose_allocate = options.get("expose_allocate", False)
        SD_calc = options.get("SD_calc", True)

        functions = {
            allocate_name: {
                "function": f"min({input_name}, {demand_name})",
                "expose": expose_allocate,
            },
            output_name: {
                "function": f"{input_name} - {allocate_name}",
                "inputs": {allocate_name: f"{self.name}.{allocate_name}.function"},
            },
        }

        if SD_calc:
            SD_name = options.get("SD_name", "SD")
            functions.update(
                {
                    SD_name: {
                        "function": f"frac_0({allocate_name}, {demand_name}, 0)",
                        "inputs": {
                            allocate_name: f"{self.name}.{allocate_name}.function"
                        },
                    }
                }
            )

        conversion_costs = self.get_parameter("conversion_costs", {})

        if conversion_costs:
            factor = conversion_costs.pop("function")
            inputs = conversion_costs.pop("inputs", {})
            output_connections = conversion_costs.pop("output_connections", {})
            function = f"{factor} * resource_in"
            functions.update(
                {
                    "conversion_costs": {
                        "function": function,
                        "inputs": {"resource_in": f"{self.name}.{input_name}"} | inputs,
                        "output_connections": {
                            "function": {
                                f"{self.name}.{allocate_name}.{input_name}",
                                f"{self.name}.{output_name}.{input_name}",
                            }
                        }
                        | output_connections,
                        "expose": False,
                    }
                }
            )

        self.add_parameters(functions=functions)
        super().initialise_object()


class Allocation(PBDMCompositeObject):
    """
    This will need to change to accomodate concurrent prioritisations
    """

    def initialise_object(self):
        components = self.get_parameter("allocation")

        for component, data in components.items():
            unit_options = data.get("options", {})
            allocation_unit = AllocationUnit(name=component, **data)
            self.add_children(allocation_unit)

            demand_name = unit_options.setdefault("demand_name", "demand")
            input_name = unit_options.setdefault("input_name", "resource_in")
            allocation_unit.add_input_connection(
                demand_name, f"metabolic_pool.demand.{component}"
            )

            SD_calc = unit_options.setdefault("SD_calc", True)
            if SD_calc:
                SD_name = unit_options.setdefault("SD_name", "SD")
                self.add_output_ports(f"{SD_name}_{component}")
                allocation_unit.add_output_connection(
                    SD_name, {f"{self.name}.{SD_name}_{component}"}
                )

        priority = list(components)
        first_name = priority[0]
        first_object = self.children[first_name]
        first_object_input_name = first_object.get_parameter("input_name", "resource_in")
        first_object.add_input_ports(first_object_input_name)
        first_object.add_input_connection(first_object_input_name, "metabolic_pool.supply.supply") 

        for i in range(len(priority) - 1):
            previous_name = priority[i]
            previous_object = self.children[previous_name]
            next_name = priority[i + 1]
            next_object = self.children[next_name]
            previous_output_name = previous_object.get_parameter(
                "output_name", "resource_out"
            )
            next_input_name = next_object.get_parameter("input_name", "resource_in")
            next_object.add_input_connection(
                next_input_name, f"allocation.{previous_name}.{previous_output_name}"
            )

        super().initialise_object()


class MetabolicPool(PBDMCompositeObject):
    def initialise_object(self):
        supply = self.get_parameter("supply")
        demand = self.get_parameter("demand")
        allocation = self.get_parameter("allocation")

        supply_object = SupplyAggregation(name="supply", supply=supply)
        demand_object = DemandAggregation(name="demand", demand=demand)
        allocation_object = Allocation(name="allocation", allocation=allocation)

        self.add_children(supply_object, demand_object, allocation_object)

        super().initialise_object()

        allocation_object.expose_outputs(self)


M = MetabolicPool(
    name="metabolic_pool",
    supply={
        "photosynthesis": {
            "leaf": "plant.leaf.photosynthesis.supply",
            "fruit": "plant.fruit.photosynthesis.supply",
        },
    },
    demand={
        "repro": {
            "fruit_bud": "plant.fruit.growth.demand",
            "fruit_rapid": "plant.fruit.growth.demand",
        },
        "growth": {
            "leaf": "plant.leaf.growth.demand",
            "stem": "plant.stem.growth.demand",
            "root": "plant.root.growth.demand",
        },
        "resp": {
            "leaf": "plant.leaf.resp.demand",
            "stem": "plant.stem.resp.demand",
            "root": "plant.root.resp.demand",
            "fruit": "plant.fruit.resp.demand",
        },
    },
    allocation={
        "resp": {
            "conversion_costs": {
                "function": 2,
            },
        },
        "repro": {},
        "growth": {},
    },
)

from pbdm.psymple_extension.psymple_connections import (
    PBDMFunctionalObject,
    PBDMCompositeObject,
)

growths = [
    PBDMFunctionalObject(name="growth", assignments=[("demand", "SD_grow")]) for i in range(5)
]
resps = [
    PBDMFunctionalObject(name="resp", assignments=[("demand", "SD_resp")]) for i in range(4)
]
leaf_photo = Function(name="photosynthesis", function="x**2", output_name="supply")
fruit_photo = Function(name="photosynthesis", function="x", output_name="supply")
root_chemo = Function(name="chemosynthesis", function="sqrt(x)", output_name="supply")

leaf = PBDMCompositeObject(name="leaf", children=[growths[0], resps[0], leaf_photo], inputs={"SD_grow": 0, "SD_resp": 0} )
root = PBDMCompositeObject(name="root", children=[growths[1], resps[1], root_chemo], inputs={"SD_grow": 0, "SD_resp": 0})
stem = PBDMCompositeObject(name="stem", children=[growths[2], resps[2]], inputs={"SD_grow": 0, "SD_resp": 0})
fruit = PBDMCompositeObject(name="fruit", children=[growths[3], resps[3], fruit_photo], inputs={"SD_grow": 0, "SD_resp": 0})
#reserves = PBDMCompositeObject(name="reserves", children=[growths[4]])

plant = PBDMCompositeObject(
    name="plant", children=[leaf, root, stem, fruit, M]
)

from pbdm.psymple_extension.draw_ported_objects import psympleGraph


plant.compile_system_connections()
X = plant.generate_ported_object()
data = X.to_data()
print("DATA", data)
"""
G = psympleGraph(data)
A = G.to_pgv()

A.layout(prog="dot", args="-Efontsize=8")
A.draw("file.svg")
"
"""
import json
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

#print("DATA", json.dumps(X.to_data(), cls=SetEncoder))
