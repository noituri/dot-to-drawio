import xml.etree.ElementTree as ET
from xml.dom import minidom

from .state import State


def is_normalized_hsv_format(color_string: str) -> bool:
    try:
        parts = color_string.split()
        if len(parts) != 3:
            return False
        h = float(parts[0])
        s = float(parts[1])
        v = float(parts[2])
        if not (0 <= h <= 1) or not (0 <= s <= 1) or not (0 <= v <= 1):
            return False
        return True
    except ValueError:
        return False


def hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    if s == 0.0:
        r = g = b = v
    else:
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
    return r, g, b


def rgb_to_hex(r: float, g: float, b: float) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def normalized_hsv_to_hex(color: tuple[float, float, float]) -> str:
    h, s, v = color
    r, g, b = hsv_to_rgb(h, s, v)
    hex_color = rgb_to_hex(r, g, b)
    return hex_color


def convert_color_string_to_hex(color_string: str) -> str:
    if is_normalized_hsv_format(color_string):
        color = tuple(map(float, color_string.split()))
        return normalized_hsv_to_hex(color)
    else:
        return color_string


def element_to_string(element: ET.Element) -> str:
    xml_string = ET.tostring(element, encoding='utf-8').decode('utf-8')
    dom = minidom.parseString(xml_string)
    return dom.toprettyxml(indent='\t')


def create_cell(state: State, root: ET.Element, parent: str = None) -> tuple[ET.Element, str]:
    cell_id = str(state.next_id)
    cell = ET.SubElement(root, "mxCell", id=cell_id)

    if parent is not None:
        cell.set("parent", parent)

    state.next_id += 1

    return cell, cell_id
