from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject

from pbdm.functions.functions import Functions

class ObjectWithFunctions(PBDMCompositeObject):
    """
    "functions": {...} <Functions object data>
    """

    def initialise_object(self):
        functions_data = self.get_parameter("functions", default={})
        name = functions_data.get("name", "functions")
        functions_object = Functions(name=name, functions=functions_data)
        self.add_children(functions_object)

        super().initialise_object()
