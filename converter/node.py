import xml.etree.ElementTree as ET

from .state import State
from .helpers import *


class Node:
    def __init__(self, s: State, obj: any):
        self.value = ""
        if '_ldraw_' in obj:
            for ldraw_obj in obj['_ldraw_']:
                if 'text' in ldraw_obj:
                    self.value += (ldraw_obj['text'].strip() + " ")
            self.value = self.value.strip()

        self.x = 0
        self.y = 0
        if 'pos' in obj:
            pos = obj['pos'].split(',')
            self.x = float(pos[0]) * s.config.xy_coef
            self.y = (s.max_height - float(pos[1])) * s.config.xy_coef

        self.width = 0
        self.height = 0
        if ('width' in obj) and ('height' in obj):
            self.width = float(obj['width']) * s.config.wh_coef
            self.height = float(obj['height']) * s.config.wh_coef

        self.shape = "ellipse"
        if 'shape' in obj and obj['shape'] == 'box':
            self.shape = obj['shape']

        self.fill_color = ""
        if 'fillcolor' in obj:
            self.fill_color = convert_color_string_to_hex(obj['fillcolor'])
        elif 'color' in obj:
            self.fill_color = convert_color_string_to_hex(obj['color'])

        self.stroke_color = "none"
        if '_draw_' in obj:
            for draw_obj in obj['_draw_']:
                if 'op' in draw_obj and draw_obj['op'] == 'c':
                    self.stroke_color = convert_color_string_to_hex(
                        draw_obj['color'])

        self.rounded = False
        if 'style' in obj:
            self.rounded = 'rounded' in obj['style']

        self.cell_id = ""

    def make_cell(self, s: State, root: ET.Element, parent: str):
        node_cell, cell_id = create_cell(s, root, parent=parent)

        self.cell_id = cell_id

        node_cell.set("value", self.value)

        style = f"whiteSpace=wrap;html=1;{self.shape};"

        if self.fill_color != "":
            style += f"fillColor={self.fill_color};"

        style += f"strokeColor={self.stroke_color};"

        if self.rounded:
            style += "rounded=1;"

        node_cell.set("style", style)

        node_cell.set("vertex", "1")

        geometry = ET.SubElement(node_cell, "mxGeometry")
        geometry.set("x", str(self.x))
        geometry.set("y", str(self.y))
        geometry.set("width", str(self.width))
        geometry.set("height", str(self.height))
        geometry.set("as", "geometry")
