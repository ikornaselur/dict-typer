# Dict-Typer

A simple tool to take a json dictionary instance and convert it into Python TypedDict class definitions

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
```

and if we run mypy on this

```shell
-> % p run mypy test.py
test.py:11: error: Unsupported operand types for + ("str" and "int")
test.py:12: error: TypedDict "NestedDictType" has no key 'non_existant'
Found 2 errors in 1 file (checked 1 source file)
```

it will immediately detect two issues!

I also want to use this project to learn more about analysing code, making sure
the project is well tested so that it's easy to experiment and try different
approaches.

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
  }
}

-> % cat .example.json | p run dt --imports
from typing import List, Union

from typing_extensions import TypedDict


class NestedDictType(TypedDict):
    number: int
    string: str

class Level3Type(TypedDict):
    number: int
    string: str

class Level2Type(TypedDict):
    level3: Level3Type

class MultipeLevelsType(TypedDict):
    level2: Level2Type

class RootType(TypedDict):
    number_int: int
    number_float: float
    string: str
    list_single_type: List[str]
    list_mixed_type: List[Union[float, int, str]]
    nested_dict: NestedDictType
    same_nested_dict: NestedDictType
    multipe_levels: MultipeLevelsType
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
   ...:   }
   ...: }
   ...:

In [2]: from dict_typer import convert

In [3]: print(convert(source, show_imports=True))
from typing import List, Union

from typing_extensions import TypedDict


class NestedDictType(TypedDict):
    number: int
    string: str

class Level3Type(TypedDict):
    number: int
    string: str

class Level2Type(TypedDict):
    level3: Level3Type

class MultipeLevelsType(TypedDict):
    level2: Level2Type

class RootType(TypedDict):
    number_int: int
    number_float: float
    string: str
    list_single_type: List[str]
    list_mixed_type: List[Union[float, int, str]]
    nested_dict: NestedDictType
    same_nested_dict: NestedDictType
    multipe_levels: MultipeLevelsType
  ```
