from __future__ import annotations

import socket
import selectors


class Client:
    def __new__(cls: type[Client]) -> Client:
        instance = super().__new__(cls)
        return instance
