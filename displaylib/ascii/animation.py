from __future__ import annotations

import os
from typing import TYPE_CHECKING, Protocol, cast

from ..template import Node
from ..template.type_hints import MroNext, NodeType
from .texture import Texture, load_texture

if TYPE_CHECKING:
    from ..template.type_hints import NodeMixin, UpdateFunction
    from .type_hints import TextureMixin
    class AnyTextureNode(TextureMixin, NodeMixin, Protocol):
        def __new__(cls, *args, **kwargs) -> AnyTextureNode: ...


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


class EmptyAnimationFrame(AnimationFrame):
    """Empty `AnimationFrame`, more like a placeholder
    """
    def __init__(self) -> None:
        self.texture = []


class Animation:
    """`Animation` containing frames

    Frames are loaded from files or partially from cache
    """
    __slots__ = ("frames")
    frames: list[AnimationFrame]

    def __init__(self, folder_path: str, /, *, reverse: bool = False, fill: bool = True, fliph: bool = False, flipv: bool = False) -> None:
        """Loads and animation with frames from either files or partially from cache

        Args:
            folder_path (str): folder path where the frames are (usually folder with .txt files)
            reverse (bool, optional): reverses the order of frames. Defaults to False.
            fill (optional, bool): fill in creeks with spaces. Defaults to True
            fliph (optional, bool): flips the texture horizontally. Defaults to False
            flipv (optional, bool): flips the texture vertically. Defaults to False
        """
        # preserve: frame0.txt -> frame10.txt -> frame15.txt
        fnames = sorted(os.listdir(folder_path), key=lambda fname: (len(fname), fname))
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
    _update: UpdateFunction
    animations: dict[str, Animation]
    frame: int = 0
    current_animation: str = ""
    is_playing: bool = False
    reverse_playback: bool = False
    _has_updated: bool = True # indicates if the first frame (per animation) has been displayed
    _accumulated_time: float = 0

    def __new__(cls: type[NodeType], *args, **animations) -> NodeType:
        mro_next = cast(MroNext[AnimationPlayer], super())
        instance = mro_next.__new__(cls, *args, force_sort=False) # because this cannot be passed as an argument, force_sort is set to False
        instance.animations = dict(animations) # make unique
        instance._update = instance._animation_player_update_wrapper(instance._update)
        return cast(NodeType, instance)

    def __init__(self, parent: AnyTextureNode, **animations: Animation) -> None:
        """Initializes the animation player

        Args:
            parent (AnyTextureNode | None, optional): parent node with Texture and Transform2D components. Defaults to None.
            **animations (Animation): animations are stored as {str: Animation, ...} pairs
        """

    @property
    def active_animation(self) -> Animation | None:
        """Returns the active Animation object

        Returns:
            Animation | None: active animaion if any active, else None
        """
        if not self.current_animation: # empty string, which is default
            return None
        return self.animations[self.current_animation]
    
    @active_animation.setter
    def active_animation(self, animation_name: str) -> None:
        """Sets the next frames based on animation name

        Args:
            animation_name (str): Animation object to be used

        Raises:
            ValueError: invalid animation name
        """
        if animation_name not in self.animations:
            raise ValueError(f"animation not found: '{animation_name}'")

        if self.parent is None or not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")

        animation = self.animations[animation_name]
        self.current_animation = animation_name
        self.frame = 0

        if not animation.frames:
            self._has_updated = True
            self.is_playing = False
            return
        
        self.is_playing = True
        self.parent.texture = animation.frames[0].texture
        self._has_updated = False
    
    def get(self, animation_name: str) -> Animation | None:
        """Returns a stored animation given its name

        Args:
            animation_name (str): name of the animation

        Returns:
            Animation | None: animation object or None if not found
        """
        return self.animations.get(animation_name, None)
    
    def add(self, animation_name: str, animation: Animation) -> None:
        """Adds a new animation and binds it to a name

        Args:
            animation_name (str): name to access the animation later
            animation (Animation): animation object to store
        """
        self.animations[animation_name] = animation
    
    def remove(self, animation_name: str) -> None:
        """Removes an animation given the name of the animation

        Args:
            animation_name (str): name of the animation to delete
        """
        del self.animations[animation_name]
    
    def play(self, animation_name: str) -> None:
        """Plays an animation given the name of the animation

        Args:
            animation (str): the name of the animation to play
        
        Raises:
            ValueError: invalid animation name
        """
        if animation_name not in self.animations:
            raise ValueError(f"animation not found: '{animation_name}'")
        
        if self.parent is None or not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")
        
        self.reverse_playback = False
        animation = self.animations[animation_name]
        self.current_animation = animation_name
        self.frame = 0

        if not animation.frames:
            self._has_updated = True
            self.is_playing = False
            return
        
        self.is_playing = True
        self.parent.texture = animation.frames[0].texture
        self._has_updated = False
    
    def play_backwards(self, animation_name: str) -> None:
        """Plays an animation backwards given the name of the animation

        Args:
            animation_name (str): the name of the animation to play backwards
        """
        if animation_name not in self.animations:
            raise ValueError(f"animation not found: '{animation_name}'")
        
        if self.parent is None or not isinstance(self.parent, Texture):
            raise TypeError("parent requires component 'Texture'")
        
        self.reverse_playback = True
        animation = self.animations[animation_name]
        self.current_animation = animation_name
        self.frame = len(animation.frames) -1

        if not animation.frames:
            self._has_updated = True
            self.is_playing = False
            return
        
        self.is_playing = True
        self.parent.texture = animation.frames[-1].texture
        self._has_updated = False
    
    def advance(self) -> bool:
        """Advances 1 frame

        Can be used in a `while loop`:
        >>> while self.my_animation_player.advance():
        >>>     ... # do stuff each frame

        Returns:
            bool: whether it continues the animation (was NOT stopped)
        """
        if self.current_animation != "" and not self.current_animation in self.animations:
            raise ValueError(f"current animation name is invalid: '{self.current_animation}'")
        
        if self.parent is None or not isinstance(self.parent, Texture):
            raise TypeError(f"parent requires component 'Texture', not '{type(self.parent).__qualname__}'")

        animation = self.animations[self.current_animation]
        
        # check playback mode and its future index
        if self.reverse_playback:
            if (self.frame -1) < 0:
                if animation.frames:
                    first_animation_frame = animation.frames[0]
                    self.parent.texture = first_animation_frame.texture
        else:
            if (self.frame +1) >= len(animation.frames):
                if animation.frames:
                    last_animation_frame = animation.frames[-1]
                    self.parent.texture = last_animation_frame.texture
                self.is_playing = False
                return False
        
        if self.reverse_playback:
            self.frame -= 1
        else:
            self.frame += 1
        animation_frame = animation.frames[self.frame]
        self.parent.texture = animation_frame.texture
        return True # returns true if not stopped

    def stop(self) -> None:
        """Stops the animation from playing
        """
        self.is_playing = False
        self._has_updated = False
    
    def _animation_player_update_wrapper(self, update_function: UpdateFunction) -> UpdateFunction:
        """Handles updating the parent's texture if an animation is playing
        """
        def _update(delta: float) -> None:
            update_function(delta)
            if self.current_animation != "" and not self.current_animation in self.animations:
                raise ValueError(f"current animation name is invalid: '{self.current_animation}'")
                
            if self.parent is None or not isinstance(self.parent, Texture):
                raise TypeError("parent requires component 'Texture'")

            if self.is_playing and self._has_updated:
                animation = self.active_animation
                if animation is not None:
                    # check playback mode and future index
                    if self.reverse_playback and (self.frame -1) >= 0:
                        self.frame -= 1
                        self.parent.texture = animation.frames[self.frame].texture
                    elif not self.reverse_playback and (self.frame +1) < len(animation.frames):
                        self.frame += 1
                        self.parent.texture = animation.frames[self.frame].texture
                    else: # both is out of bounds, therefore, stop
                        self.is_playing = False

            elif not self._has_updated:
                self._has_updated = True
        return _update
