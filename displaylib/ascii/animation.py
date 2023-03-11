from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator

from ..template import Node
from . import grapheme
from .types import ModeFlags

if TYPE_CHECKING:
    from .surface import ASCIISurface


__all__ = [
    "Frame",
    "Animation",
    "EmptyAnimation",
    "AnimationPlayer"
]


class Frame:
    __slots__ = ("content")

    def __init__(self, fpath: str, fliph: bool = False, flipv: bool = False) -> None:
        self.content = []
        f = open(fpath)
        for line in f.readlines():
            self.content.append(list(line.rstrip("\n")))
        if fliph:
            self.content = grapheme.mapfliph(self.content)
        if flipv:
            self.content = grapheme.mapfliph(self.content)
            
        f.close()


class Animation:
    __slots__ = ("frames")

    def __init__(self, path: str, reverse: bool = False, fliph: bool = False, flipv: bool = False) -> None:
        fnames = os.listdir(path)
        step = 1 if not reverse else -1
        self.frames = [Frame(os.path.join(path, fname), fliph=fliph, flipv=flipv) for fname in fnames][::step]


class EmptyAnimation(Animation):
    __slots__ = ("frames")

    def __init__(self) -> None:
        self.frames = []


class AnimationPlayer(Node): # TODO: add buffered animations on load
    FIXED = 0 # TODO: implement FIXED and DELTATIME mode
    # DELTATIME = 1

    def __init__(self, parent: Node | None = None, fps: float = 16, mode: ModeFlags = FIXED, **animations) -> None:
        super().__init__(parent, force_sort=False)
        self.fps: float = fps
        self.mode = mode # process mode (FIXED | DELTATIME)
        self.animations: dict[str, Animation] = dict(animations)
        self.current_animation: str = ""
        self.is_playing: bool = False
        self._current_frames: Generator | None = None
        self._next: None | Frame = None
        self._has_updated: bool = False # indicates if the first frame (per animation) have been displayed
        self._accumulated_time: float = 0.0
    
    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        try:
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
    
    def get(self, name: str) -> Animation:
        return self.animations[name]
    
    def add(self, name: str, animation: Animation) -> None:
        self.animations[name] = animation
    
    def remove(self, name: str) -> None:
        del self.animations[name]
    
    def play(self, animation: str) -> None:
        """Plays an animation given the name of the animation

        Args:
            animation (str): the name of the animation to play
        """
        self.is_playing = True
        self.current_animation = animation
        self._current_frames = (frame for frame in self.animations[animation].frames)
        try:
            self._next: Frame = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next: Frame = None
        if self._next != None:
            self.parent.content = self._next.content
            self._has_updated = False
    
    def play_backwards(self, animation: str) -> None:
        """Plays an animation backwards given the name of the animation

        Args:
            animation (str): the name of the animation to play backwards
        """
        self.is_playing = True
        self.current_animation = animation
        # reverse order frames
        self._current_frames = (frame for frame in reversed(self.animations[animation].frames))
        try:
            self._next: Frame = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next: Frame = None
        if self._next != None:
            self.parent.content = self._next.content
            self._has_updated = False
        
    def advance(self) -> bool:
        """Advances 1 frame

        Can be used in a `while loop`:
        >>> while self.my_animation_player.advance():
        ...     ... # do stuff each frame

        Returns:
            bool: whether it was NOT stopped
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
        if frame != None:
            self.parent.content = frame.content
            self._has_updated = False
        return frame != None # returns true if not stopped


    def stop(self) -> None:
        """Stops the animation from playing
        """
        self.is_playing = False

    def _render(self, surface: ASCIISurface) -> None: # dummy method
        return

    def _update(self, delta: float) -> None:
        if self.is_playing and self._has_updated:
            # if self.mode == AnimationPlayer.FIXED:
            frame = next(self)
            if frame == None:
                return
            self.parent.content = frame.content

            # elif self.mode == AnimationPlayer.DELTATIME:
            #     # apply delta time
            #     self._accumulated_time += delta
            #     if self._accumulated_time >= self._fps_ratio:
            #         self._accumulated_time -= self._fps_ratio # does not clear time
            #         frame = next(self)
            #         self.owner.content = frame.content
        elif not self._has_updated:
            self._has_updated = True
