from pbdm.population_processes.population_processes import PopulationProcesses
from pbdm.population_dynamics.population_dynamics import PopulationDynamics
from pbdm.metabolic_pool.metabolic_pool import MetabolicPool

from pbdm.functions.functions import Functions, Function

from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

class FunctionalPopulation(PBDMCompositeObject):
    """
    Functional Population

    - bdfs
    - processes
    - dynamics
    - metabolic pool
    
    """
    def initialise_object(self):
        sub_populations = self.get_parameter("sub_populations", {}, search_ancestry=False)
        for name, population_data in sub_populations.items():
            stage_structure = self.get_parameter(f"stage_structure.{name}", {})
            stage_structure.update(ancestor=self.name)
            #print("PASSSTR", stage_structure)
            population_data.update(stage_structure=stage_structure)
            functional_population = FunctionalPopulation(name=name, **population_data)
            self.add_children(functional_population)

        # Controls whether structures are inherited from parent (default not)
        inherit_structure = self.get_parameter("inherit_structure", {})
        objects_with_variables = []
        
        bdfs = self.get_parameter("bdfs", {}, inherit_structure.get("bdfs", False))
        if bdfs:
            bdfs_object = Functions(name="bdfs", functions=bdfs)
            self.add_children(bdfs_object)

        processes = self.get_parameter("processes", {}, inherit_structure.get("processes", False))
        print(self.name, processes)
        if processes:
            processes_object = PopulationProcesses(name="processes", processes=processes)
            self.add_children(processes_object)
            objects_with_variables.append(processes_object)

        stage_structure = self.get_parameter("stage_structure", {}, search_ancestry=False)
        #stage_structure.update(ancestor=self.name)
        dynamics = self.get_parameter("dynamics", {}, inherit_structure.get("dynamics", False))
        print(self.name, dynamics)
        if dynamics:
            dynamics_object = PopulationDynamics(name="dynamics", dynamics=dynamics, stage_structure=stage_structure)
            self.add_children(dynamics_object)
            objects_with_variables.append(dynamics_object)

        metabolic_pool = self.get_parameter("metabolic_pool", {}, inherit_structure.get("metabolic_pool", False))
        if metabolic_pool:
            metabolic_pool_object = MetabolicPool(name="metabolic_pool", **metabolic_pool)
            self.add_children(metabolic_pool_object)

        super().initialise_object()

        for object in objects_with_variables:
            object.expose_variables(self)




"""
stage_structure = {
    "ancestor": <>,
    <next_stage>: <stage_name>,
    OR
    "next_stage": {
        "stage_1": {
            "rate": <function>
            "inputs": <>
        },

    }                       

}


"""
"""
food_source = Function(name="source", function="2", output_name="supply")

fly = FunctionalPopulation(
    name="fly",
    age_structure={
        "k": 3,
        "Del": 30,
        "variable": "A",
        "index_function": "(i-0.5)*Del/k"
    },
    bdfs = {
        "growth_rate": {
            "function": "TEMP**2 + 1"
        } 
    },
    processes = {
        "growth": {
            "type": "age_structured_demand_population_process",
            "rate": {
                "function": "SD*growth_rate / a",
                "inputs": {"SD": "fly.metabolic_pool.allocation.growth_SD", "a": 0.02},
            }
        }
    },
    dynamics = {
        "number": {
            "type": "distributed_delay",
            "variable_name": "n",
        }
    },
    metabolic_pool = {
        "demand": {
            "growth": {
                "fly": "fly.processes.growth.demand"
            }
        },
        "supply": {
            "food_source": {
                "food": "system.source.supply"
            }
        },
        "allocation": {
            "growth": {
                "conversion_costs": {
                    "function": 0.2
                }
            }
        }
    }
)

system = PBDMCompositeObject(name="system", children=[fly, food_source])

system.compile_system_connections()
X= system.generate_ported_object()
print(X.to_data())

"""