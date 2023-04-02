from __future__ import annotations

import re
from ast import literal_eval
 
from . import class_register


class DeserializeError(TypeError): ...


def is_float_str(string: str) -> bool:
    pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    match = re.match(pattern, string)
    return bool(match)

def is_bool_str(string: str) -> bool:
    return string == "True" or string == "False"

def is_list_str(string: str) -> bool:
    return string.startswith("[") and string.endswith("]")

def is_dict_or_set_str(string: str) -> bool:
    return string.startswith("{") and string.endswith("}")

def is_tuple_str(string: str) -> bool:
    return string.startswith("(") and string.endswith(")")

def is_none_str(string: str) -> bool:
    return string == "None"

def is_unknown(string: str) -> bool:
    return True

def construct_unknown(encoded: str) -> object:
    """Tries to construct a class from class name and arguments 

    Args:
        encoded (str): string to decode

    Raises:
        DeserializeError: invalid argument when creating an instance of a class

    Returns:
        object: instance based on the information contained in argument `encoded`
    """
    name, _delimiter, arguments = encoded[:-1].partition("(") # TODO: make more flexible
    if not name in class_register.cache:
        return encoded # is most likely of type str
    cls = class_register.cache[name]
    solution = getattr(cls, "__deserialize__", None)
    if solution:
        # format of variable `arguments`: "arg1, arg2, arg3", where each arg can end with either "=" or "!"
        return solution(arguments)
    # fallback onto creating an instance based on the __recipe__ response protocol
    args = []
    kwargs = {}
    modifications = {}
    for argument in arguments.split(", "):
        if "!" in argument:
            attr, _delimiter, value = argument.partition("!")
            modifications[attr] = literal_eval(value)
            continue
        elif "=" in argument and argument[0] != "=":
            key, _delimiter, value = argument.partition("=")
            kwargs[key] = literal_eval(value)
            continue
        else:
            args.append(literal_eval(argument))
    try:
        instance = cls(*args, **kwargs)
    except Exception as error:
        raise DeserializeError(f"could not create instance of type '{cls.__qualname__}', with arguments '...(*{tuple(args)}, **{kwargs})'") from error
    for name, value in modifications.items():
        setattr(instance, name, value)
    return instance

# recognition function: solution function -> instance
convertion = {
    str.isdigit: int,
    is_float_str: float,
    is_bool_str: bool,
    is_list_str: literal_eval,
    is_dict_or_set_str: literal_eval,
    is_none_str: lambda _string: None,
    is_unknown: construct_unknown
}


def deserialize(encoded: str, /) -> object:
    """Tries to deserialize the encoded instance. Can revert the `__recipe__` protocol

    Args:
        encoded (str): encoded instance containing class name and attributes to recreate

    Returns:
        object: best match for the serialized object

    Raises:
        DeserializeError: instance could not be created from given arguments
    """
    for recognition, solution in convertion.items():
        if recognition(encoded):
            return solution(encoded)
