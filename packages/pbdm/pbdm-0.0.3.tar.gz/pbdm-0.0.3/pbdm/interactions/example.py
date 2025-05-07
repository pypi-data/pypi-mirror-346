from pbdm.functional_population.functional_population import FunctionalPopulation
#from pbdm.interactions.interactions import Interaction
from pbdm.population_processes.basic_population_process import PopulationProcess

rabbit = FunctionalPopulation(
    name="rabbit",
    bdfs = {
        "growth_rate": {
            "function": "0.4"
        }
    },
    dynamics={
        "numbers": {
            "variable_name": "x",
        }
    },
    processes={
        "growth": {
            "type": "population_process",
            "rates": {
                "number_growth": {
                    "function": "r*x",
                    "inputs": {"r": "rabbit.bdfs.growth_rate", "x": "growth.variables.x"},
                }
            },
            "variables": {
                "x": {
                    "function": "number_growth",    
                    "variable": "x" 
                },  
            },
            "variable_connections": {"x": {"rabbit.dynamics.numbers.x", "rabbit.r"}}
            #"variable_connections": {"x": {"rabbit.dynamics.numbers.x", "rabbit.r"}},
        }
    },
    variable_ports=["r"],
)

fox = FunctionalPopulation(
    name="fox",
    bdfs = {
        "death_rate": {
            "function": "-0.2",
        },
        "predation_rate": {
            "function": "0.05",
        }
    },
    dynamics={
        "numbers": {
            "variable_name": "x",
        }
    },
    processes={
        "death": {
            "type": "population_process",
            "rates": {
                "number_death": {
                    "function": "r*x",
                    "inputs": {"r": "fox.bdfs.death_rate", "x": "death.variables.x"},
                }
            },
            "variables": {
                "number": {
                    "function": "number_death",
                    "variable": "x",
                }
            },
            "variable_connections": {"x": {"fox.f", "fox.dynamics.numbers.var"}}
            #"variable_connections": {"x": {"fox.dynamics.numbers.x", "fox.f"}},
        }
    },
    variable_ports=["f"],
)

interaction = PopulationProcess(
    name="interaction",
    rates = {
        "response": {
            "function": "a*r*f",
            "inputs": {"r": "system.rabbit.r", "f": "system.fox.f", "a": "system.fox.bdfs.predation_rate"},
            #"structured_inputs": {...},
        }
    },
    variables = {
        "r": {
            "function": " - response",
            "variable": "r",
            "scalars": {"neg": "-1"},
        },
        "f": {
            "function": "response",
            "variable": "f",
            "scalars": {"metabolic_cost": "1/2"},
        }
    },
    variable_connections = {"r": {"system.rabbit.r", "system.r"}, "f": {"system.fox.f", "system.f"}},
)

"""
interaction = Interaction(
    name="rabbit_fox",
    consumer="system.fox",
    resource="system.rabbit",
    consumer_variable="f",
    resource_variable="r",
    functional_response={
        "function": "r*fox*rabbit",
        "inputs": {
            "r": "system.fox.bdfs.predation_rate",
            "fox": "rabbit_fox.odes.f",
            "rabbit": "rabbit_fox.odes.r",
        },
    },
    variable_ports = ["f", "r"],
    variable_connections = {
            "f": {"system.fox.dynamics.numbers.x"},
            "r": {"system.rabbit.dynamics.numbers.x"},
        },
)
"""

from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

system = PBDMCompositeObject(
    name="system",
    children=[rabbit, fox, interaction],
    variable_ports=["r", "f"],
)

from pbdm.psymple_extension.draw_ported_objects import psympleGraph

system.compile_system_connections()
X = system.generate_ported_object()
data = X.to_data()
print(data)

"""
G = psympleGraph(data)
A = G.to_pgv()

A.layout(prog="dot", args="-Efontsize=8")
A.draw("file.pdf")


from psymple.build import System

S = System(X, compile=True)

print(S)

sim = S.create_simulation(initial_values={"r": 10, "f": 2})

sim.simulate(t_end=100)
sim.plot_solution()
"""

#### BUG: fox creates a spurious dummy variable port, but rabbit doesn't. WHY? No effect on model.
#### FIXED!
