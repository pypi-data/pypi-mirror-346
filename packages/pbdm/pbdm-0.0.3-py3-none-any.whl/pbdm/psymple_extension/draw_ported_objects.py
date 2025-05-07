# import networkx as nx
import sys, os, pathlib

if sys.platform == "win32":
    path = pathlib.Path(r"C:\Program Files\Graphviz\bin")
    if path.is_dir() and str(path) not in os.environ["PATH"]:
        os.environ["PATH"] += f";{path}"

import pygraphviz as pgv

from psymple.build import HIERARCHY_SEPARATOR
from psymple.build.ported_objects import PortedObjectData

import itertools as it
import matplotlib.pyplot as plt


class psympleGraph:
    def __init__(self, ported_object_data: dict, level: int = 2):

        ported_object_data = PortedObjectData(**ported_object_data)

        graph_data = self.convert_data(ported_object_data, max_level=level)

        self.graph_data = graph_data

        """
        input_ports = ported_object_data.data.get("input_ports", [])
        for port in input_ports:
            port_name = port.get("name")
            directed_nodes.append(port_name)
        """

        """
        directed_wires = object_data.get("directed_wires")
        directed_edges = []
        for wire in directed_wires:
            source = wire.get("source").split(HIERARCHY_SEPARATOR)[0]
            destinations = [destination.split(HIERARCHY_SEPARATOR)[0] for destination in wire.get("destinations")]
            for destination in destinations:
                if source in self.child_nodes and destination in self.child_nodes:
                    directed_edges.append((source, destination))
        self.directed_edges = directed_edges

        super().__init__(self.directed_edges)
        #super().add_nodes_from(["A", "B"], size=10)
        #super().add_edges_from(self.directed_edges)
        """

    def convert_data(self, data, max_level=2, level=0):
        graph_data = {}
        if level < max_level:
            children = data.data.get("children", [])
            if children:
                if level < max_level - 1:
                    graph_data["children"] = {}
                    for child in children:
                        child_data = PortedObjectData(**child)
                        graph_data["children"][child_data.name] = self.convert_data(
                            child_data, max_level, level + 1
                        )
                else:
                    graph_data["children"] = self.convert_children(data)

                graph_data["variable_edges"] = self.convert_variable_wires(data)
                graph_data["directed_edges"] = self.convert_directed_wires(data)

            graph_data["variable_nodes"] = self.convert_directed_nodes(data)
            graph_data["directed_nodes"] = self.convert_variable_nodes(data)

        return graph_data

    def convert_children(self, data):
        children_data = data.data.get("children", [])
        children_names = {
            PortedObjectData(**child_data).name for child_data in children_data
        }

        return children_names

    def convert_directed_nodes(self, data):
        inputs = data.data.get("input_ports", [])
        outputs = data.data.get("output_ports", [])
        directed_nodes = {node.get("name") for node in inputs + outputs}

        return directed_nodes

    def convert_variable_nodes(self, data):
        variables = data.data.get("variable_ports", [])
        variable_nodes = {node.get("name") for node in variables}

        return variable_nodes

    def convert_directed_wires(self, data):
        directed_wires = data.data.get("directed_wires", [])
        directed_edges = {}
        directed_edges["in"] = {}
        directed_edges["out"] = {}
        directed_edges["internal"] = {}
        for wire in directed_wires:
            source = wire.get("source")
            destinations = wire.get("destinations")
            internal_destinations = [
                dest
                for dest in destinations
                if HIERARCHY_SEPARATOR in source and HIERARCHY_SEPARATOR in dest
            ]
            if internal_destinations:
                directed_edges["internal"][source] = internal_destinations
            out_destinations = [
                dest for dest in destinations if HIERARCHY_SEPARATOR not in dest
            ]
            if out_destinations:
                directed_edges["out"][source] = out_destinations
            in_destinations = [
                dest for dest in destinations if HIERARCHY_SEPARATOR not in source
            ]
            if in_destinations:
                directed_edges["in"][source] = in_destinations

        return directed_edges

    def convert_variable_wires(self, data):
        variable_wires = data.data.get("variable_wires", [])
        variable_edges = {}
        for wire in variable_wires:
            parent = wire.get("parent_port")
            children = wire.get("child_ports")
            variable_edges[parent] = children

        return variable_edges

    def to_pgv(self):
        """
        WARNING: only works for 2 recursions currently
        """
        G = pgv.AGraph(strict=False)
        graph_data = self.graph_data

        child_data = graph_data.get("children", {})

        for cluster, cluster_data in child_data.items():
            grandchild_nodes = set()
            grandchildren = cluster_data.get("children", {})
            for grandchild in grandchildren:
                node_name = f"obj_{cluster}.{grandchild}"
                grandchild_nodes.add(node_name)
                G.add_node(node_name, label=grandchild, fontsize=10)

            G.add_subgraph(
                grandchild_nodes, name=f"cluster{cluster}", label=cluster, fontsize=12
            )

            directed_nodes = cluster_data.get("directed_nodes", {})
            variable_nodes = cluster_data.get("variable_nodes", {})

            port_nodes = directed_nodes | variable_nodes
            for node in port_nodes:
                node_name = f"port_{cluster}.{node}"
                G.add_node(
                    node_name,
                    label=f"{cluster}.{node}",
                    shape="box",
                    height=0.1,
                    width=0.1,
                    fontsize=8,
                )

            directed_edges_internal = cluster_data.get("directed_edges", {}).get("internal", {})
            for source, destinations in directed_edges_internal.items():
                # print("WIRE", source, destinations)
                source_obj, source_port = source.split(HIERARCHY_SEPARATOR)
                source_name = f"obj_{cluster}.{source_obj}"
                for destination in destinations:
                    dest_obj, dest_port = destination.split(HIERARCHY_SEPARATOR)
                    destination_name = f"obj_{cluster}.{dest_obj}"
                    G.add_edge(
                        source_name,
                        destination_name,
                        dir="forward",
                        headlabel=dest_port,
                        taillabel=source_port,
                        arrowsize=0.5,
                    )

            directed_edges_out = cluster_data.get("directed_edges", {}).get("out", {})
            for source, destinations in directed_edges_out.items():
                source_obj, source_port = source.split(HIERARCHY_SEPARATOR)
                source_name = f"obj_{cluster}.{source_obj}"
                for destination in destinations:
                    destination_name = f"port_{cluster}.{destination}"
                    G.add_edge(
                        source_name,
                        destination_name,
                        dir="forward",
                        taillabel=source_port,
                        arrowsize=0.5,
                    )

            directed_edges_in = cluster_data.get("directed_edges", {}).get("in", {})
            # print("DIREDIN", directed_edges_in)
            for source, destinations in directed_edges_in.items():
                source_name = f"port_{cluster}.{source}"
                for destination in destinations:
                    dest_obj, dest_port = destination.split(HIERARCHY_SEPARATOR)
                    destination_name = f"obj_{cluster}.{dest_obj}"
                    G.add_edge(
                        source_name,
                        destination_name,
                        dir="forward",
                        headlabel=dest_port,
                        arrowsize=0.5,
                    )

            variable_edges = cluster_data.get("variable_edges", {})
            for parent, children in variable_edges.items():
                source_name = f"port_{cluster}.{parent}"
                for child in children:
                    destination_obj, destination_port = child.split(HIERARCHY_SEPARATOR)
                    destination_name = f"obj_{cluster}.{destination_obj}"
                    G.add_edge(
                        source_name,
                        destination_name,
                        dir="both",
                        style="dashed",
                        arrowsize=0.5,
                        arrowhead="obox",
                        arrowtail="obox",
                        headlabel=destination_port,
                    )

        directed_edges_internal = graph_data.get("directed_edges", {}).get("internal", {})

        for source, destinations in directed_edges_internal.items():
            # source_obj, source_port = source.split(HIERARCHY_SEPARATOR)
            source_name = f"port_{source}"
            for destination in destinations:
                destination_name = f"port_{destination}"
                G.add_edge(source_name, destination_name, dir="forward", arrowsize=0.5)

        return G

    def get_data(self, data, level):
        name = data.get("metadata").get("name")
        if name == level:
            return data
        else:
            children = data.get("object_data").get("children", [])
            for child in children:
                data = self.get_data(child, level)
                if data:
                    return data



