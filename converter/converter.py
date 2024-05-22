import graphviz
import json
import xml.etree.ElementTree as ET

from .config import Config
from .node import Node
from .edge import Edge
from .state import State
from .helpers import *


class Converter:
    def __init__(self, config: Config):
        self.state = State(config)

    def convert(self, dot_graph: str) -> str:
        source = graphviz.Source(dot_graph)
        source_json = json.loads(source.pipe('json').decode())

        self.state.next_id = 0
        self.state.max_height = float(source_json['bb'].split(',')[-1])

        model = ET.Element("mxGraphModel")
        root = ET.SubElement(model, "root")
        _, root_cell_id = create_cell(self.state, root)
        _, nodes_cell_id = create_cell(self.state, root, parent=root_cell_id)

        self.state.is_directed = source_json['directed']

        nodes = {}

        for obj in source_json['objects']:
            node = Node(self.state, obj)
            node.make_cell(self.state, root, nodes_cell_id)
            nodes[obj['_gvid']] = node

        for edge in source_json['edges']:
            if '_draw_' not in edge:
                continue

            edge_obj = Edge(edge)
            source = nodes[edge_obj.tail]
            target = nodes[edge_obj.head]
            edge_obj.make_cell(self.state, root, nodes_cell_id, source, target)

        return element_to_string(model)
