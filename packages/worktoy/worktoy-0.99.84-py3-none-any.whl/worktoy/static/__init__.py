"""The 'worktoy.static' module provides low level parsing and casting
utilities. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from . import casting
from ._this import THIS, OWNER, ATTR, Zeroton
from ._deleted import DELETED
from ._type_sig import TypeSig
from ._dispatch import Dispatch
from ._overload import overload

__all__ = [
    'THIS',
    'OWNER',
    'ATTR',
    'Zeroton',
    'DELETED',
    'TypeSig',
    'Dispatch',
    'overload',
    'casting',
]
