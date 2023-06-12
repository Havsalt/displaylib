# DisplayLib

### An `object-oriented` framework for displaying `ASCII` graphics and creating an `infinite world`, aimed at `simplifying the process`

---
### Requires Python `version` >= `3.10`
---

## Submodules
- `template`
- `ascii` (default)
- `pygame`
---

## Example using displaylib
```python
import displaylib as dl # using `ascii` mode as default


class Square(dl.Node2D, dl.Texture): # using a node class in conjunction with the component `dl.Texture`
    self.texture = [ # you can use this style to define its visual
        [*"OO+OO"], # the "+" here represents transparancy
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
        dl.Screen.cell_transparant = "+" # set what represents transparancy
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
    # autoruns on instance creation
    app = App(tps=4, width=24, height=8)
```

---


## Networking support
DisplayLib provides mixin classes for enabling networking. Networking is available in each submodule through `dl.networking` (when using `import displaylib.[mode] as dl`).

To create a `Client`, use:
```python
class MyApp(dl.Engine, dl.Client): ...
```
Creating a `Server` is as simple as:
```python
class MyServer(dl.Engine, dl.Server): ...
```

---

Example using `displaylib` in `ascii` mode:
```python 
import displaylib.ascii as dl
# mode selected   ^^^^^


class Square(dl.Sprite): # using `dl.Sprite`, as it derives from `dl.Node`, `dl.Transform2D` and `dl.Texture`
    self.texture = [
        [*"OO+OO"],
        [*"O+++O"],
        [*"OO+OO"]
    ]

    def _update(self, delta: float) -> None:
        if len(self.texture[1]) == 5:
            self.texture[1].append(")")
        else:
            self.texture[1].pop()
    

class App(dl.Engine):
    def _on_start(self) -> None:
        # -- config
        dl.Screen.cell_transparant = "+"
        dl.Screen.cell_default = "."
        # -- create nodes
        self.my_square = Square(x=5, y=3)
        self.direction = 1
    
    def _update(self, delta: float) -> None:
        if self.direction == 1:
            self.my_square.position.x += 1
            if self.my_square.position.x == 22:
                self.direction = -1
        elif self.direction == -1:
            self.my_square.position.x -= 1
            if self.my_square.position.x == 4:
                self.direction = 1

if __name__ == "__main__":
    app = App(tps=4, width=24, height=8)

```
---

Example using `displaylib` in `pygame` mode:
```python 
import displaylib.pygame as dl
# mode selected   ^^^^^^
import pygame # import pygame

import random
import math


class Cirlce(dl.Node2D):
    def __init__(self, parent: dl.Node | None = None, x: int = 0, y: int = 0) -> None:
        super().__init__(parent, x, y)
        self.radius = 20
        self.width = 2
        self.time_elapsed = 0.0
    
    def _update(self, delta: float) -> None:
        self.time_elapsed += delta
        self.width = round(math.cos(self.time_elapsed) * 3 +5)
    
    def _render(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (200, 50, 255), (self.position.x, self.position.y), self.radius, self.width)


class App(dl.Engine):
    def _on_start(self) -> None:
        print("= Started Pygame program")
        self.circle = Cirlce(x=200, y=100)
        self.elapsed_time = 0.0
    
    def _update(self, delta: float) -> None:
        self.circle.position = dl.Vec2(
            math.cos(self.elapsed_time) * 50,
            math.sin(self.elapsed_time) * 50
        ) + dl.Vec2i(200, 100)
        self.elapsed_time += delta
    
    def _render(self, surface: pygame.Surface) -> None:
        pygame.draw.line(surface, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), start_pos=(50, 50), end_pos=(200, 100), width=5)


if __name__ == "__main__":
    app = App("Pygame example using DisplayLib")

```
