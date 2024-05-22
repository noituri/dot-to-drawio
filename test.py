from converter import Config
from converter import Converter


config = Config(3.0, 100.0)

dot_string = """
graph graphname {
    a -- b -- c;
    b -- d;
}
"""

result = Converter(config).convert(dot_string)
print(result)
