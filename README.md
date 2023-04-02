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


class Square(dl.Node2D, dl.Texture):
    def __init__(self, parent: dl.Node | None = None, x: int = 0, y: int = 0) -> None:
        super().__init__(parent, x, y) # the most important arguments to pass down
        self.texture = [ # you can use this style to define its visual
            [*"OO+OO"], # the "+" represents transparancy
            [*"O+++O"], # changed through `dl.Node2D.cell_transparancy`
            [*"OO+OO"]
        ]

    def _update(self, delta: float) -> None: # called every frame
        if len(self.texture[1]) == 5: # modifying the middle line
            self.texture[1].append(")")
        else:
            self.texture[1].pop()
    

class App(dl.Engine):
    def _on_start(self) -> None: # use this instead of __init__
        # -- config
        dl.Screen.cell_transparant = "+" # represents transparancy
        dl.Screen.cell_default = "." # changes background default
        # -- create nodes
        self.my_square = Square(x=5, y=3)
        # nodes are kept alive by `Node.nodes` (dict) by default
        # this means `del self.my_square` is needed to fully free it
        self.direction = 1
    
    def _update(self, delta: float) -> None: # called every frame
        if self.direction == 1:
            self.my_square.position.x += 1
            if self.my_square.position.x == 22:
                self.direction = -1
        elif self.direction == -1:
            self.my_square.position.x -= 1
            if self.my_square.position.x == 4:
                self.direction = 1

if __name__ == "__main__":
    # autorun on instance creation
    app = App(tps=4, width=24, height=8)

```