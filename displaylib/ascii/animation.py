from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator, cast

from ..template import Node
from ..template.type_hints import MroNext, NodeType
from .texture import Texture, load_texture

if TYPE_CHECKING:
    from ..template.type_hints import AnyNode


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
        self.texture = load_texture(fpath, fill=fill, fliph=fliph, flipv=flipv)


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
        fnames = os.listdir(folder_path)
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
    animations: dict[str, Animation]
    current_animation: str
    is_playing: bool
    _current_frames: Generator[AnimationFrame, None, None] | None
    _next: AnimationFrame | None
    _has_updated: bool
    _accumulated_time: float

    def __new__(cls: type[NodeType], *args, **animations) -> NodeType:
        mro_next = cast(MroNext[AnimationPlayer], super())
        instance = mro_next.__new__(cls, *args, force_sort=False) # because this cannot be passed as an argument, force_sort is set to False
        instance.animations = dict(animations)
        instance.current_animation = ""
        instance.is_playing = False
        instance._current_frames = None
        instance._next = None
        instance._has_updated = False # indicates if the first frame (per animation) has been displayed
        instance._accumulated_time = 0.0
        return cast(NodeType, instance)

    def __init__(self, parent: AnyNode | None = None, **animations: Animation) -> None:
        """Initializes the animation player

        Args:
            parent (ValidTextureNode | None, optional): parent node with Texture and Transform2D components. Defaults to None.
            **animations (Animation): animations are stored as {str: Animation, ...} pairs

        Raises:
            TypeError: 'parent' missing component Texture
        """

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
        if not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")
        if self._next is not None and self.parent is not None:
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
        if not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")
        if self._next is not None and self.parent is not None:
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
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
        if not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")
        if self._next is not None and self.parent is not None:
            self.parent.texture = self._next.texture
            self._has_updated = False
        return self._next != None # returns true if not stopped

    def stop(self) -> None:
        """Stops the animation from playing
        """
        self.is_playing = False
    
    def _update(self, _delta: float) -> None:
        """Handles updating the parent's texture if an animation is playing
        """
        if self.is_playing and self._has_updated:
            frame = next(self)
            if not isinstance(self.parent, Texture):
                raise TypeError("parent requires component 'Texture'")
            if frame is None or self.parent is None:
                return
            self.parent.texture = frame.texture
        elif not self._has_updated:
            self._has_updated = True
