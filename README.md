# Dict-Typer

A simple tool to take a json dictionary instance and convert it into Python TypedDict class definitions

## Example

```
-> % cat test.json
{
  "id": 1241,
  "summary": "This is a summary",
  "fraction": 0.181,
  "items": ["list", "with", "items"],
  "mixed": ["mixed", "items", 1, "as", "well", 0.15]
}

-> % cat test.json | p run dt
class RootType(TypedDict):
    id: int
    summary: str
    fraction: float
    items: List[str]
    mixed: List[Union[float, int, str]]
```
