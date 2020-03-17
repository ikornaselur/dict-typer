# Dict-Typer

A simple tool to take a json dictionary instance and convert it into Python TypedDict class definitions

## Example

```
-> % echo '{"number": 123, "text": "hello, world", "fraction": 0.12}' | dt
class RootType(TypedDict):
    number: int
    text: str
    fraction: float
```
