from __future__ import annotations

import os

from ..math import Vec2i
from ..template import Node, Client
from .surface import ASCIISurface
from .clock import Clock
from .node import ASCIINode2D


class ASCIIClient(Client):
    def _main_loop(self) -> None:
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index

        nodes = tuple(Node.nodes.values())
        clock = Clock(self.tps)
        while self.is_running:
            delta = 1.0 / self.tps
            self.screen.clear()
            
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[id(node)]
            Node._queued_nodes.clear()
            
            if self.auto_resize_screen:
                terminal_size = os.get_terminal_size()
                if ((terminal_size.columns - self.screen_margin.x) != self.screen.width) or ((terminal_size.lines - self.screen_margin.y) != self.screen.height):
                    self.screen.width = int(terminal_size.columns - self.screen_margin.x)
                    self.screen.height = int(terminal_size.lines - self.screen_margin.y)
                    size = Vec2i(terminal_size.columns, terminal_size.lines)
                    for node in nodes:
                        if isinstance(node, ASCIINode2D):
                            node._on_screen_resize(size)
                    os.system("cls")
            
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())

            # render content of visible nodes onto a surface
            self.screen.rebuild(Node.nodes.values(), self.screen.width, self.screen.height)
            
            self._render(self.screen)
            # nodes can render custon data onto the screen
            for node in nodes:
                if isinstance(node, ASCIINode2D):
                    node._render(self.screen)
            
            self.screen.show()
            self._update_socket()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        surface = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.show()