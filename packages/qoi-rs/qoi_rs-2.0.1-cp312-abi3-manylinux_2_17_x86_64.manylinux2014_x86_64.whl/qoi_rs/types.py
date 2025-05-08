from collections.abc import Sequence
from typing import Literal, Protocol, runtime_checkable

__all__ = "Data", "Image"

type Data = (
    Sequence[tuple[int, int, int]]
    | Sequence[tuple[int, int, int, int]]
    | Sequence[int]
    | bytes
    | bytearray
)

type ColourSpace = Literal["SRGB", "linear"]

type Mode = Literal["RGB", "RGBA"]

@runtime_checkable
class Image(Protocol):
    @property
    def width(self) -> int: pass
    @property
    def height(self) -> int: pass
    @property
    def data(self) -> bytes: pass
    @property
    def channels(self) -> int: pass
    @property
    def colour_space(self) -> ColourSpace: pass
    @property
    def mode(self) -> Mode: pass
