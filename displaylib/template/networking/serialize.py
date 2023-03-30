from __future__ import annotations

import re
from ast import literal_eval

from ...math import Vec2, Vec2i


class SerializeError(TypeError): ...


def is_float_str(string: str) -> bool:
    pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    match = re.match(pattern, string)
    return bool(match)

def is_bool_str(string: str) -> bool:
    return string == "True" or string == "False"

def is_vec2_str(string: str) -> bool: # TODO: move into ripper function
    return string.startswith("Vec2(") and string.endswith(")")

def is_vec2i_str(string: str) -> bool: # TODO: move into ripper function
    return string.startswith("Vec2i(") and string.endswith(")")

def is_list_str(string: str) -> bool:
    return string.startswith("[") and string.endswith("]")

def is_dict_or_set_str(string: str) -> bool:
    return string.startswith("{") and string.endswith("}")

def is_tuple_str(string: str) -> bool:
    return string.startswith("(") and string.endswith(")")

def is_none_str(string: str) -> bool:
    return string == "None"

# TODO: add rip/extract function to get class name and args to construct


convertion = {
    str.isdigit: int,
    is_float_str: float,
    is_bool_str: bool,
    is_list_str: literal_eval,
    is_dict_or_set_str: literal_eval,
    is_none_str: lambda _string: None,
    is_vec2_str: Vec2,
    is_vec2i_str: Vec2i
}


def serialize(instance: object) -> str:
    """Calls the underlaying `__serialize__` on argument `instance`.
    If not found, tries to serialize based on `__recipe__`
    
    ----
    #### Syntax of `__recipe__`:
        * `"[attr]"`  positional argument
        * `"[attr]="` keyword argument
        * `"[attr]!"` attribute is set after instance creation

    Args:
        instance (SupportsSerialize): instance to serialize

    Returns:
        str: serialized string
    """
    if hasattr(instance, "__serialize__"):
        return instance.__serialize__()
    
    elif instance.__class__.__module__ == "builtins":
        return str(instance)
    
    # alternative to implementing `__serialize__` (using `__recipe__`)
    elif hasattr(instance, "__recipe__"): # uses important attributes to recreate an instance
        arg_values = []
        kwarg_values = []
        modification_values = []
        for instruction in getattr(instance, "__recipe__"):
            attr, suffix, = instruction, ""
            if "!" in instruction:
                attr, suffix, _ = instruction.partition("!")
            else:
                attr, suffix, _ = instruction.partition("=")
            # do stuff
            if suffix == "!":
                value = attr + suffix + str(getattr(instance, attr))
                modification_values.append(value)
            elif suffix == "=":
                value = attr + suffix + str(getattr(instance, attr))
                kwarg_values.append(value)
            else:
                value = str(getattr(instance, attr))
                arg_values.append(value)
        values = (*arg_values, *kwarg_values, *modification_values)
        return f"{instance.__class__.__qualname__}({', '.join(values)})"
    raise SerializeError(f"instance of class '{instance.__class__.__qualname__}' missing either __serialized__ or __recipe__, or is not a builtin type")


def deserialize(value: str) -> object:
    """Deserializes the value given

    Args:
        value (str): string representation of a builtin, custom class or Vec2/Vec2i

    Returns:
        object: _description_
    """
    for recognition, solution in convertion.items():
        if recognition(value):
            return solution(value)
