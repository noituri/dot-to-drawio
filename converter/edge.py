import xml.etree.ElementTree as ET

from .state import State
from .helpers import *
from .node import Node


class Edge:
    def __init__(self, obj):
        self.value = ""
        if 'label' in obj:
            self.value = obj['label']

        self.tail = obj["tail"]
        self.head = obj["head"]

        self.stroke_color = ""
        if 'color' in obj:
            self.stroke_color = convert_color_string_to_hex(obj['color'])

    def make_cell(self, s: State, root: ET.Element, parent: str, source: Node, target: Node):
        node_cell, _ = create_cell(s, root, parent=parent)
        node_cell.set("value", f"{self.value}")
        node_cell.set("edge", "1")
        node_cell.set("source", source.cell_id)
        node_cell.set("target", target.cell_id)

        style = ""

        if not s.is_directed:
            style += "endArrow=none;"

        if self.stroke_color != "":
            style += f"strokeColor={self.stroke_color};"

        node_cell.set("style", style)

        geometry = ET.SubElement(node_cell, "mxGeometry")
        geometry.set("relative", "1")
        geometry.set("as", "geometry")
