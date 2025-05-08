from . import types

def encode(data: types.Data, /, *, width: int, height: int, colour_space: types.ColourSpace = None) -> bytes:
    pass

def decode(data: bytes, /) -> types.Image:
    pass

__all__ = "encode", "decode"
