from .distributed_delay import DistributedDelay
from .variables import PopulationVariable

from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

class PopulationDynamics(PBDMCompositeObject):
    """
    Container class for population dynamics objects. Currently assumed to be Distributed Delays.

    There is default exposure of dynamics information.
    """
    def initialise_object(self):
        children = self.get_parameter("dynamics", search_ancestry=False)
        for child, data in children.items():
            type = data.pop("type", "population_variable")
            if type == "distributed_delay":
                child_object = DistributedDelay(name=child, **data)
            elif type == "population_variable":
                child_object = PopulationVariable(name=child, **data)
            else:
                raise Exception(f"Unknown population dynamics module {type}")
            self.add_children(child_object)
        
        super().initialise_object()

        child_object.expose_variables(self)

