from pbdm.population_processes.basic_population_process import MultiPopulationProcess, AgeStructuredPopulationProcess
from pbdm.functions.functions import Function, AgeStructuredIntegral, AgeStructuredFunction


class DemandPopulationProcess(MultiPopulationProcess):
    """
    Required inputs:
        - rate
        - functions ({})
        - var_name ("var")

    Searched inputs:
        - demand_name ("demand")
        - SD_name ("SD")

    """

    def initialise_object(self):
        rate_data = self.get_parameter("rate", search_ancestry=False)
        rate_function = rate_data.pop("function")
        demand_name = self.get_parameter("demand_name", default="demand")

        demand_rate_object = Function(name="demand_rate", function=rate_function)
        self.add_children(demand_rate_object)

        SD_name = self.get_parameter("SD_name", default="SD")
        SD_adjusted_rate = "*".join([rate_function, SD_name])

        rate_data.update({"function": SD_adjusted_rate})
        self.add_parameters(rate=rate_data)
        super().initialise_object()

        self.add_output_ports(demand_name)
        demand_rate_object.add_output_connection(
            "function", {f"{self.name}.{demand_name}"}
        )

        # Input for SD is automatically created


class AgeStructuredDemandPopulationProcess(AgeStructuredPopulationProcess):
    def initialise_object(self):
        rate_data = self.get_parameter("rate", search_ancestry=False)
        rate_function = rate_data.pop("function")

        demand_name = self.get_parameter("demand_name", default="demand")
        rate_function_object = AgeStructuredFunction(
            name="age_demand_rate", function=rate_function
        )

        self.add_output_ports(demand_name)
        demand_integral = AgeStructuredIntegral(
            name="demand_integral",
            integrand="age_demand",
            integrand_inputs={"age_demand": f"{self.name}.age_demand_rate.function"},
            output_name="integral",
            output_connections={"integral": {f"{self.name}.{demand_name}"}},
        )

        self.add_children(rate_function_object, demand_integral)
        SD_name = self.get_parameter("SD_name", default="SD")
        preference_function = self.get_parameter(
            "preference_function", default="1", search_ancestry=False
        )
        SD_adjusted_rate = "*".join([rate_function, SD_name, preference_function])
        rate_data.update({"function": SD_adjusted_rate})

        self.add_parameters(rate=rate_data)
        super().initialise_object()


ADP = AgeStructuredDemandPopulationProcess(
    "growth",
    age_structure={"k": 3, "variable": "A", "index_function": "(i-0.5)*Del/k"},
    rate={"function": "M_0 * exp(c*A)"},
    preference_function="6/(Del**2) * A * (Del - A)",
)

#ADP.compile_system_connections()
#X = ADP.generate_ported_object()

#print(X.to_data())
