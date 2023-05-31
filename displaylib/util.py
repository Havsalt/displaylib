from __future__ import annotations

import types
from typing import TypeVar

Self = TypeVar("Self")
T = TypeVar("T")


template_source_code = """
def __new__(cls, *args, {keyword_arguments_or_empty}**kwargs):
    return super(cls).__thisclass__.mro()[1].__new__(cls, *args, **kwargs)
"""


def pull(*arguments: str):
    """Constructs `__new__` for the decorated class. Required when adding new arguments to `__init__`
    
    When implementing a Player class that takes `health` as argument in `__init__`, use `@dl.pull("health")`.
    This will construct a `__new__` for the Player class.
    #### Example:
    
    >>> import displaylib.ascii as dl
    >>> @dl.pull("health")
    >>> class Player(dl.Node2D):
    >>>     def __init__(self, parent=None, x=0, y=0, health=5):
    >>>         super().__init__(parent, x=x, y=y)
    >>>         self.health = health
    
    #### This will create a `__new__` that looks something like this:

    >>> def __new__(cls, *args, health=None, **kwargs):
    >>>     return super().__new__(cls, *args, **kwargs)
    """
    def decorator(cls: T) -> T:
        # prevent overriding __new__ if it exists
        if "__new__" in cls.__dict__:
            raise TypeError(f"cannot construct dunder '__new__' nor pull arguments because it is already implemented for {cls}")
        # parse argument names
        keyword_arguments = "".join(arg + "=None, " for arg in arguments)
        modified_source_code = template_source_code.format(keyword_arguments_or_empty=keyword_arguments)
        # compile and retrieve the compiled __new__ function
        compiled_code = compile(modified_source_code, filename="<string>", mode="exec")
        namespace = {}
        exec(compiled_code, namespace)
        new_function = namespace["__new__"]
        # bind and set function as method
        new_method = types.MethodType(new_function, cls)
        setattr(cls, "__new__", new_method)
        return cls
    return decorator
