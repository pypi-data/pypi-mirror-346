from pbdm.population_processes.basic_population_process import PopulationProcess, BasicPopulationProcess
#from .demand_population_process import DemandPopulationProcess, AgeStructuredDemandPopulationProcess

from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

process_classes = {
     "population_process": PopulationProcess,
     "basic_process": BasicPopulationProcess
     #"demand_population_process": DemandPopulationProcess,
     #"age_structured_demand_population_process": AgeStructuredDemandPopulationProcess,
}

class PopulationProcesses(PBDMCompositeObject):
     def initialise_object(self):
        processes = self.get_parameter("processes", {})
        for process, data in processes.items():
            type = data.get("type", "population_process")
            ProcessClass = process_classes.get(type)
            process_object = ProcessClass(name=process, **data)
            self.add_children(process_object)

        super().initialise_object()

        for process in self.children.values():
            process.expose_variables(self)


P = PopulationProcesses(
    name="processes",
    age_structure={"k": 3},
    processes = {
          "mortality": {
               "type": "population_process",
               "rates": {
                    "number_mortality": {
                         "type": "age_structured",
                         "function": "mort_bdf*n",
                         #"age_structured_inputs": {"mort_bdf": "pop.bdfs.temp_mortality", "n": "mortality.variables.n"}
                    }
               },
               "variables": {
                    "n": {
                         "type": "age_structured",
                         "function": "number_mortality",
                         #"age_structured_variables": {"n": {"larvae.dynamics.number.n"}},
                    }
               },
          }
     },
)

#P.compile_system_connections()
#X = P.generate_ported_object()
#data = X.to_data()
#print(data)