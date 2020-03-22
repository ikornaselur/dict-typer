# Dict-Typer

A simple tool to take a json dictionary instance and convert it into Python TypedDict class definitions

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
