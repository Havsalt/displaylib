from __future__ import annotations

import io
import os
import functools
from typing import TYPE_CHECKING, Generator, cast

from ..template import Node
from . import text
from .texture import Texture

if TYPE_CHECKING:
    from ..template.type_hints import Self


EMPTY = " " # filler when load_frame_texture(..., fill=True)

@functools.cache
def load_frame_texture(file_path: str, /, *, fill: bool = True, fliph: bool = False, flipv: bool = False) -> list[list[str]]:
    file: io.TextIOWrapper = open(file_path, "r") # from disk
    texture = [list(line.rstrip("\n")) for line in file.readlines()]
    if fill:
        longest = len(max(texture, key=len))
        lines = len(texture)
        for line in texture:
            if len(line) < longest:
                diff = longest - len(line)
                line.extend(list(EMPTY*diff))
        if len(texture) < lines:
            diff = lines - len(texture)
            texture.extend(list(EMPTY*longest) for _ in range(diff))
    if fliph:
        texture = text.mapfliph(texture)
    if flipv:
        texture = text.mapfliph(texture)
    file.close()
    return texture


class AnimationFrame:
    """`AnimationFrame` used to create animations

    Loaded at runtime from files or from cache
    """
    __slots__ = ("texture")

    def __init__(self, file_path: str, /, *, fill: bool = True, fliph: bool = False, flipv: bool = False) -> None:
        """Loads the texture for the frame from either a file or from cache

        Args:
            file_path (str): file path to load from
            fill (optional, bool): fill in creeks with spaces. Defaults to True
            fliph (optional, bool): flips the texture horizontally. Defaults to False
            flipv (optional, bool): flips the texture vertically. Defaults to False
        """
        fpath = os.path.normpath(file_path)
        self.texture = load_frame_texture(fpath, fill=fill, fliph=fliph, flipv=flipv)


class Animation:
    """`Animation` containing frames

    Frames are loaded from files or partially from cache
    """
    __slots__ = ("frames")

    def __init__(self, folder_path: str, /, *, reverse: bool = False, fill: bool = True, fliph: bool = False, flipv: bool = False) -> None:
        """Loads and animation with frames from either files or partially from cache

        Args:
            folder_path (str): folder path where the frames are (usually folder with .txt files)
            reverse (bool, optional): reverses the order of frames. Defaults to False.
            fill (optional, bool): fill in creeks with spaces. Defaults to True
            fliph (optional, bool): flips the texture horizontally. Defaults to False
            flipv (optional, bool): flips the texture vertically. Defaults to False
        """
        fnames = os.listdir(os.path.join(os.getcwd(), folder_path))
        step = 1 if not reverse else -1
        self.frames = [AnimationFrame(os.path.join(os.getcwd(), folder_path, fname), fill=fill, fliph=fliph, flipv=flipv) for fname in fnames][::step]


class EmptyAnimation(Animation):
    """Empty `Animation`, more like a placeholder
    """
    __slots__ = ("frames")

    def __init__(self) -> None:
        """Initializes the empty animation with no frames
        """
        self.frames = []


class AnimationPlayer(Node):
    """`AnimationPlayer` that plays animations, changing the `.texture` attribute of the parent

    Parent Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
        - `Texture`: changes its texture
    
    Known Issues:
        - `If a file's content is changed after a texture has been loaded from that file, the change won't be reflected on next load due to the use of @functools.cache`
    """
    def __new__(cls: type[Self], *args, **animations) -> Self: # pulling: `**animations`
        return super().__new__(cls, *args, force_sort=False) # because this cannot be passed as an argument, force_sort is set to False

    def __init__(self, parent: Node | None = None, **animations: Animation) -> None:
        """Initializes the animation player

        Args:
            parent (ValidTextureNode | None, optional): parent node with Texture and Transform2D components. Defaults to None.
            **animations (Animation): animations are stored as {str: Animation, ...} pairs

        Raises:
            TypeError: 'parent' missing component Texture
        """
        # if parent is None or not isinstance(parent, Texture):
        #     raise TypeError(f"parent in AnimationPlayer cannot be '{type(parent)}' (requires Texture in MRO)")
        super().__init__(parent=cast(Node | None, parent), force_sort=False)
        self.animations: dict[str, Animation] = dict(animations)
        self.current_animation: str = ""
        self.is_playing: bool = False
        self._current_frames: Generator[AnimationFrame, None, None] | None = None
        self._next: AnimationFrame | None = None
        self._has_updated: bool = False # indicates if the first frame (per animation) has been displayed
        self._accumulated_time: float = 0.0
    
    def __iter__(self: Self) -> Self:
        """Use itself as main iterator

        Returns:
            AnimationPlayer: itself
        """
        return self

    def __next__(self) -> AnimationFrame | None:
        """Returns the next frame from the current frames (a generator)

        Returns:
            AnimationFrame: the next frame
        """
        try:
            if self._current_frames is None:
                return None
            self._next = next(self._current_frames) # next of generator
            return self._next
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
            return None

    @property
    def active_animation(self) -> Animation | None:
        """Returns the active Animation object

        Returns:
            Animation | None: active animaion if any active, else None
        """
        return self.animations.get(self.current_animation, None)
    
    @active_animation.setter
    def active_animation(self, animation: str) -> None:
        """Sets the next frames based on animation name

        Args:
            animation (str): Animation object to be used
        """
        self.current_animation = animation
        # make generator
        self._current_frames = (frame for frame in self.animations[animation].frames)
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
    
    def get(self, name: str) -> Animation | None:
        """Returns a stored animation given its name

        Args:
            name (str): name of the animation

        Returns:
            Animation | None: animation object or None if not found
        """
        return self.animations.get(name, None)
    
    def add(self, name: str, animation: Animation) -> None:
        """Adds a new animation and binds it to a name

        Args:
            name (str): name to access the animation later
            animation (Animation): animation object to store
        """
        self.animations[name] = animation
    
    def remove(self, name: str) -> None:
        """Removes an animation given the name of the animation

        Args:
            name (str): name of the animation to delete
        """
        del self.animations[name]
    
    def play(self, animation: str) -> None:
        """Plays an animation given the name of the animation

        Args:
            animation (str): the name of the animation to play
        """
        self.is_playing = True
        self.current_animation = animation
        # make generator
        self._current_frames = (frame for frame in self.animations[animation].frames)
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
        if self._next is not None and self.parent is not None and isinstance(self.parent, Texture):
            self.parent.texture = self._next.texture
            self._has_updated = False
    
    def play_backwards(self, animation: str) -> None:
        """Plays an animation backwards given the name of the animation

        Args:
            animation (str): the name of the animation to play backwards
        """
        self.is_playing = True
        self.current_animation = animation
        # reverse order frames generator
        self._current_frames = (frame for frame in reversed(self.animations[animation].frames))
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
        if self._next is not None and self.parent is not None and isinstance(self.parent, Texture):
            self.parent.texture = self._next.texture
            self._has_updated = False
    
    def advance(self) -> bool:
        """Advances 1 frame

        Can be used in a `while loop`:
        >>> while self.my_animation_player.advance():
        >>>     ... # do stuff each frame

        Returns:
            bool: whether it continues the animation (was NOT stopped)
        """
        if self._current_frames == None:
            return False
        frame = self._next
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
        if frame is not None and self.parent is not None and isinstance(self.parent, Texture):
            self.parent.texture = frame.texture
            self._has_updated = False
        return frame != None # returns true if not stopped

    def stop(self) -> None:
        """Stops the animation from playing
        """
        self.is_playing = False
    
    def _update(self, _delta: float) -> None:
        """Handles updating the parent's texture if an animation is playing
        """
        if self.is_playing and self._has_updated:
            frame = next(self)
            if frame == None or self.parent is None or not isinstance(self.parent, Texture):
                return
            self.parent.texture = frame.texture
        elif not self._has_updated:
            self._has_updated = True
