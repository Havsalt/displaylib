from __future__ import annotations

from ...math import Vec2, Vec2i
from ...template.type_hints import NodeType
from ..node import AsciiNode2D
from ..texture import Texture, load_texture

from ..camera import AsciiCamera
from ..debug import debug


# class ParallexLayer:
#     __slots__ = ("texture", "z_index")
#     z_index: int
#     texture: list[list[str]]

#     @classmethod
#     def load(cls, file_path: str, /, z_index: int = 0) -> ParallexLayer:
#         instance = cls(z_index=z_index)
#         instance.texture = load_texture(file_path)
#         return instance

#     def __init__(self, texture: list[list[str]] = [], z_index: int = 0) -> None:
#         self.texture = texture
#         self.z_index = z_index
    
#     def size(self) -> Vec2i:
#         longest = len(max(self.texture, key=len))
#         lines = len(self.texture)
#         return Vec2i(longest, lines)


from ..prefabs.sprite import AsciiSprite

class ParallexLayer(AsciiSprite): # DEV STRUCT
    z_depth: int = 0 # DEV
    centered = True # DEV


class ParallexSprite(AsciiNode2D):
    z_index: int = 0
    scalar: float = 10
    layers: list[ParallexLayer]

    def __new__(cls: type[NodeType], *args, z_index: int = 0, **kwargs) -> NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: ParallexSprite  # type: ignore
        instance.z_index = z_index
        instance.layers = []
        Texture._instances.append(instance) # type: ignore
        return instance # type: ignore

    def add_layer(self, layer: ParallexLayer) -> None:
        layer.parent = self # TEMP
        self.layers.append(layer)
    
    def _get_final_texture(self) -> list[list[str]]:
        # return [] # DISABLED
        longest = 0
        lines = 0
        for layer in self.layers:
            if (layer_longest := len(max(layer.texture, key=len))) > longest:
                longest = layer_longest
            if (layer_lines := len(layer.texture)) > lines:
                lines = layer_lines
        texture: list[list[str]] = [list(self.root.screen.cell_transparant * longest)
                                    for _ in range(lines)]
        # seen from above
        diff = AsciiCamera.current.get_global_position() - self.get_global_position()
        origin = Vec2(0, 0)
        # for layer in sorted(self.layers, key=lambda layer: layer.z_index):
        for layer in self.layers:
            # horizontal - x
            layer_fake_position_horizontal = Vec2(layer.z_depth, diff.x)
            x_scalar = layer_fake_position_horizontal.direction_to(origin).y
            # debug(idx, x_scalar, label=str(layer.uid))
            layer.position.x = x_scalar * self.scalar
            # vertical - y
            # layer_fake_position_horizontal = Vec2(layer.z_depth, diff.y)
            # y_scalar = -layer_fake_position_horizontal.direction_to(origin).y
            # debug(idx, y_scalar, label=str(layer.uid))
            # layer.position.y = y_scalar * self.scalar
        return texture

    def _get_texture_global_position(self) -> Vec2:
        return self.get_global_position()
    
    def queue_free(self) -> None:
        Texture._instances.remove(self) # type: ignore
        super().queue_free()
        # TEMP
        for layer in self.layers:
            layer.queue_free()
