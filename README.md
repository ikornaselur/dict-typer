# Dict-Typer

A simple tool to take a json payload and convert it into Python TypedDict class
definitions

## Why is this useful?

When dealing with API responses, you're very likely to be using JSON responses,
and you might have deeply nested dictionaries, lists of items and it can be
slightly hard to wrap your head around the structure of the responess you are
working with. The first thing I usually do it try to create some data structure
around it so that I can benefit from linting and typing information in my code.

Now this tends to be time consuming and error prone, so I thought it might be a
good idea to automate this process with a tool for the future. Just as an
example, if we take the output generated from the Example section below and
imagine it's a response we get from an api. We can plug it in like this:

```python
from project.types import RootType


def get_from_api() -> RootType:
    pass


def run() -> None:
    response = get_from_api()

    test1 = response["nested_dict"]["number"] + 1
    test2 = response["nested_dict"]["string"] + 1
    test3 = response["nested_dict"]["non_existant"] + 1
    for item in response["optional_items"]:
        print(item + 1)
```

and if we run mypy on this

```shell
-> % poetry run mypy test.py
test.py:43: error: Unsupported operand types for + ("str" and "int")
test.py:44: error: TypedDict "NestedDictType" has no key 'non_existant'
test.py:46: error: Unsupported operand types for + ("None" and "int")
test.py:46: error: Unsupported operand types for + ("str" and "int")
test.py:46: note: Left operand is of type "Union[None, int, str]"
Found 4 errors in 1 file (checked 1 source file)
```

it will immediately detect four issues!

I also want to use this project to learn more about analysing code, making sure
the project is well tested so that it's easy to experiment and try different
approaches.

## Usage

Either supply a path to a file or pipe json output to `dict-typer`

```help
-> % dict-typer --help
Usage: dict-typer [OPTIONS] [FILE]...

Options:
  --imports / --no-imports  Show imports at the top, default: True
  --help                    Show this message and exit.

-> % dict-typer ./.example.json
...

-> % curl example.com/test.json | dict-typer
...
```

## TypeDict definitions

There are two ways to define a TypedDict, the primary one that uses the class
based structure, as seen in the examples here. It's easier to read, but it has
a limitation that the each key has to be avalid identifier and not a reserved
keyword. Normally that's not an issue, but if you have for example, the
following data

```json
{
    "numeric-id": 123,
    "from": "far away",
}
```

which is valid json, but has the invalid identifier `numeric-id` and reserved
keyword `from`, meaning the definition

```python
class RootType(TypedDict):
    numeric-id: int
    from: str
```

is invalid. In detected cases, dict-typer will use an [alternative
way](https://www.python.org/dev/peps/pep-0589/#alternative-syntax) to define
those types, looking like this

```python
RootType = TypedDict('TypedDict', {'numeric-id': int, 'from': str'})
```

which is not as readable, but valid.

dict-typer by default only uses the alternative definition for the types with
invalid keys.

## Lists

If the root of the payload is a list, it will be treated just like a list
within a dictionary, where each item is parsed and definitions created for sub
items. In these cases, a type alias is added as well to the output to capture
the type of the list. For example, the list `[1, "2", 3.0, { "id": 123 }, {
"id": 456 }]` will generate the following definitions:

```python
from typing_extensions import TypedDict


class RootItemType(TypedDict):
    id: int

RootType = List[Union[RootItemType, float, int, str]]
```

## Examples

### Calling from shell

```shell
-> % cat .example.json
{
  "number_int": 123,
  "number_float": 3.0,
  "string": "string",
  "list_single_type": ["a", "b", "c"],
  "list_mixed_type": ["1", 2, 3.0],
  "nested_dict": {
    "number": 1,
    "string": "value"
  },
  "same_nested_dict": {
    "number": 2,
    "string": "different value"
  },
  "multipe_levels": {
    "level2": {
      "level3": {
        "number": 3,
        "string": "more values"
      }
    }
  },
  "nested_invalid": { "numeric-id": 123, "from": "far away" },
  "optional_items": [1, 2, "3", "4", null, 5, 6, null]
}

-> % cat .example.json | dict-typer
from typing import List, Union

from typing_extensions import TypedDict


class NestedDictType(TypedDict):
    number: int
    string: str


class Level2Type(TypedDict):
    level3: NestedDictType


class MultipeLevelsType(TypedDict):
    level2: Level2Type


NestedInvalidType = TypedDict("NestedInvalidType", {
    "numeric-id": int,
    "from": str,
})


class RootType(TypedDict):
    number_int: int
    number_float: float
    string: str
    list_single_type: List[str]
    list_mixed_type: List[Union[float, int, str]]
    nested_dict: NestedDictType
    same_nested_dict: NestedDictType
    multipe_levels: MultipeLevelsType
    nested_invalid: NestedInvalidType
    optional_items: List[Union[None, int, str]]
```

### Calling from Python
```python
In [1]: source = {
   ...:   "number_int": 123,
   ...:   "number_float": 3.0,
   ...:   "string": "string",
   ...:   "list_single_type": ["a", "b", "c"],
   ...:   "list_mixed_type": ["1", 2, 3.0],
   ...:   "nested_dict": {
   ...:     "number": 1,
   ...:     "string": "value"
   ...:   },
   ...:   "same_nested_dict": {
   ...:     "number": 2,
   ...:     "string": "different value"
   ...:   },
   ...:   "multipe_levels": {
   ...:     "level2": {
   ...:       "level3": {
   ...:         "number": 3,
   ...:         "string": "more values"
   ...:       }
   ...:     }
   ...:   },
   ...:   "nested_invalid": { "numeric-id": 123, "from": "far away" },
   ...:   "optional_items": [1, 2, "3", "4", None, 5, 6, None]
   ...: }
   ...:

In [2]: from dict_typer import get_type_definitions

In [3]: print(get_type_definitions(source, show_imports=True))
from typing import List, Union

from typing_extensions import TypedDict


class NestedDictType(TypedDict):
    number: int
    string: str


class Level2Type(TypedDict):
    level3: NestedDictType


class MultipeLevelsType(TypedDict):
    level2: Level2Type


NestedInvalidType = TypedDict("NestedInvalidType", {
    "numeric-id": int,
    "from": str,
})


class RootType(TypedDict):
    number_int: int
    number_float: float
    string: str
    list_single_type: List[str]
    list_mixed_type: List[Union[float, int, str]]
    nested_dict: NestedDictType
    same_nested_dict: NestedDictType
    multipe_levels: MultipeLevelsType
    nested_invalid: NestedInvalidType
    optional_items: List[Union[None, int, str]]
```
