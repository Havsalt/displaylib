# Displaylib

### A collection of frameworks used to display ASCII or Pygame graphics
### Requires Python version >= 3.10
---

## Submodules
- `template`
- `ascii` (default)
- `pygame`
---

Example using `displaylib` in `ascii` mode:
```python 
import displaylib.ascii as dl
# mode selected   ^^^^^


class Square(dl.Node2D):
    def __init__(self, parent: dl.Node | None = None, x: int = 0, y: int = 0) -> None:
        super().__init__(parent, x, y) # the most important args to pass down
        self.content = [ # you can use this style to define its visual
            [*"OO+OO"], # the "+" represents transparancy
            [*"O+++O"], # changed through `dl.Node2D.cell_transparancy`
            [*"OO+OO"]
        ]
    
    def _update(self, delta: float) -> None:
        # access engine namespaces with `self.root.[namespace]`
        if self.position.x > self.root.screen.width:
            return # guard statement
        self.position.x += 1 # moves the square by 1 on the x-axis


class App(dl.Engine):
    def _on_ready(self) -> None: # use this instead of __init__
        # -- config
        dl.Node2D.cell_transparent = "+" # represents transparancy
        dl.Node2D.cell_default = "." # changes background default
        # -- create nodes
        self.my_square = Square(x=5, y=3)
        # nodes are kept alive by `Node.nodes` (dict) by default
        # this means `del self.my_square` is needed to fully free it
    
    def _update(self, delta: float) -> None:
        ... # called every frame


if __name__ == "__main__":
    # autorun on instance creation
    app = App(tps=4, width=24, height=8)

```