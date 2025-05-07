from pbdm.population_dynamics.variables import ODESystem, ODE, DifferentialEquations

from pbdm.functions.functions import AgeStructuredIntegral, Function, AgeStructuredFunction

from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

from sympy import parse_expr

from pbdm.age_structure.age_structure import AgeStructuredObject


class DistributedDelayDifferentialEquations(ODESystem, AgeStructuredObject):
    def initialise_object(self):
        k = self.get_parameter("age_structure.k")
        variable_name = self.get_parameter("variable", self.name)

        odes = {f"{variable_name}_1": f" - DD_rate_1 * {variable_name}_1"} | {
            f"{variable_name}_{i}": f"DD_rate_{i} * ({variable_name}_{i-1} - {variable_name}_{i})"
            for i in range(2, k + 1)
        }

        self.add_parameters(odes=odes)
        super().initialise_object()
        AgeStructuredObject.initialise_object(self)


class DistributedDelay(PBDMCompositeObject, AgeStructuredObject):
    def initialise_object(self):
        # k = self.get_parameter("age_structure.k")
        dd_odes_name = f"{self.name}_odes"

        k = self.get_parameter("age_structure.k")
        rate_data = self.get_parameter("rate", default={"function": "k/Del"})
        parse_rate_function = parse_expr(rate_data.get("function"))
        sub_parse_rate_function = parse_rate_function.subs("k", k)
        rate_data["function"] = str(sub_parse_rate_function)
        rate_object = AgeStructuredFunction(name="rate", **rate_data)

        DD_ODEs = DistributedDelayDifferentialEquations(
            name=dd_odes_name,
            age_structured_inputs={"DD_rate": f"{self.name}.rate.function"},
        )
        print(f"child of {self.name} is {dd_odes_name}")
        self.add_children(rate_object, DD_ODEs)

        # for i in range(1, k + 1):
        #    port_name = f"{variable_name}_{i}"
        #    self.add_variable_ports(port_name)
        #    self.add_variable_connection(port_name, {f"{dd_odes_name}.{port_name}"})

        calculations = self.get_parameter(
            "calculations", default={}, search_ancestry=False
        )
        variable_name = self.get_parameter("variable", self.name)

        for calculation, data in calculations.items():
            type = data.get("type")
            if type == "integral":

                calc_object = AgeStructuredIntegral(
                    name=calculation,
                    integrand="x",
                    integrand_inputs={
                        "x": f"{self.name}.{dd_odes_name}.{variable_name}"
                    },
                    output_name="output",
                    **data,  ##???
                )
                self.add_children(calc_object)
                self.add_output_ports(calculation)
                calc_object.add_output_connection(f"output", {f"{calculation}.output"})

        stage_structure = self.get_parameter("stage_structure", {})
        print("STAGE", stage_structure)
        if stage_structure:
            odes_object = ODE(
                name="out_odes",
                function=f"DD_rate*{variable_name}",
                variable=f"{variable_name}_out",
                inputs={
                    "DD_rate": f"{self.name}.rate.function_{k}",
                    f"{variable_name}": f"{self.name}.{dd_odes_name}.{variable_name}_{k}",
                },
            )
            next_stage = stage_structure.get("next_stage", {})
            ancestor = stage_structure.get("ancestor", {})
            # Should be target_object.get("variable") rather than self's variable name

            if isinstance(next_stage, str):
                target_address = (
                    f"{ancestor}.{next_stage}.dynamics.{self.name}.{variable_name}"
                )
                self.add_variable_connection(f"{variable_name}_out", {target_address})
            elif isinstance(next_stage, dict):
                odes = {}
                for stage, split_function in next_stage.items():
                    ode_data = dict(
                        function=f"DD_rate*{variable_name}*{split_function.get('rate', '1')}",
                        variable=f"{variable_name}_out_{stage}",
                        inputs={
                            "DD_rate": f"{self.name}.rate.function_{k}",
                            f"{variable_name}": f"{self.name}.{dd_odes_name}.{variable_name}_{k}",
                        }
                        | split_function.get("inputs", {}),
                    )
                    odes.update({f"out_{stage}": ode_data})
                    target_variable = split_function.get("target_variable", variable_name)
                    target_address = (
                    f"{ancestor}.{stage}.dynamics.{self.name}.{target_variable}"
                    )
                    self.add_variable_connection(f"{variable_name}_out_{stage}", {target_address})
                odes_object = DifferentialEquations(name="out_odes", odes=odes)

            self.add_children(odes_object)
        super().initialise_object()
        if stage_structure:
            odes_object.expose_variables(self)
        DD_ODEs.expose_variables(self)

        AgeStructuredObject.initialise_object(self)


dyn_egg = PBDMCompositeObject(
    name="dynamics",
    children=[
        DistributedDelay(
            name="DDTM",
            variable_name="M",
            # variable_connections={"M_out": {}},
        )
    ],
    variable_ports=[f"M_{i}" for i in range(1, 3 + 1)] + ["M_out"],
    variable_connections={f"M_{i}": {f"DDTM.M_{i}"} for i in range(1, 4)},
)
dyn_larv = PBDMCompositeObject(
    name="dynamics",
    children=[DistributedDelay(name="DDTM", variable_name="M")],
    variable_ports=[f"M_{i}" for i in range(1, 3 + 1)] + ["M_out"],
    variable_connections={f"M_{i}": {f"DDTM.M_{i}"} for i in range(1, 4)},
)
dyn_diap = PBDMCompositeObject(
    name="dynamics",
    children=[DistributedDelay(name="DDTM", variable_name="M")],
    variable_ports=[f"M_{i}" for i in range(1, 3 + 1)] + ["M_out"],
    variable_connections={f"M_{i}": {f"DDTM.M_{i}"} for i in range(1, 4)},
)

egg = PBDMCompositeObject(
    name="egg",
    Del=40,
    children=[dyn_egg],
    stage_structure={"next_stage": "diap", "ancestor": "fly"},
)
larv = PBDMCompositeObject(name="larv", Del=60, children=[dyn_larv], stage_structure={"next_stage": "diap", "ancestor": "fly"})
diap = PBDMCompositeObject(name="diap", Del=1000, children=[dyn_diap])


fly = PBDMCompositeObject(
    name="fly",
    age_structure={"k": 3},
    children=[egg, larv, diap],
    variable_ports=["M_start"],
    variable_connections={"M_start": {"egg.dynamics.DDTM.DDTM_odes.M_1"}},
)

"""
fly.compile_system_connections()
X = fly.generate_ported_object()
data = X.to_data()
print(data)

from psymple.build import System

S = System(X, compile=True)

print(S)

sim = S.create_simulation(initial_values={"M_start": 10})

sim.simulate(t_end=50)
sim.plot_solution()
"""

# DD = DistributedDelay(name="mass", age_structure={"k": 3}, variable_name="M", calculations={"total": {"type": "integral"}})

# DD.initialise_object()
# DD.compile_system_connections()
# X = DD.generate_ported_object()

# print(X.to_data())
