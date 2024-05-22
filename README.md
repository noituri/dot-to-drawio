# Dot to Drawio

Example usage:

```py
config = Config(3.0, 100.0)

dot_string = """
graph graphname {
    a -- b -- c;
    b -- d;
}
"""

result = Converter(config).convert(dot_string)
print(result)
```

Authors:
- Jacek Gołębiowski
- Kamil Kochańczyk
- Mikołaj Radkowski
