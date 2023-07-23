from __future__ import annotations as _annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .template.type_hints import AnyEngine

__all__ = [
    "autorun"
]

autorun = lambda app: app()
