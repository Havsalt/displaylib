from __future__ import annotations


class SerializeError(TypeError): ...


def serialize(instance: object, /) -> str:
    """Calls the underlaying `__serialize__` on argument `instance`.
    If not found, tries to serialize based on `__recipe__`,
    which can only have arguments of builtin types (if used in `deserialize`)
    
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
    # alternative to implementing `__serialize__` (using `__recipe__`)
    if hasattr(instance, "__recipe__"): # uses important attributes to recreate an instance
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
    else:
        solution = getattr(instance, "__serialize__", None)
        if solution:
            return solution()
        
        elif instance.__class__.__module__ == "builtins":
            return str(instance)
    
    raise SerializeError(f"instance of class '{instance.__class__.__qualname__}' missing either __serialize__ or __recipe__, or is not a builtin type")
