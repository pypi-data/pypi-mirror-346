# qoi-rs

Python library made using [qoi](https://crates.io/crates/qoi) and [pyo3](https://crates.io/crates/pyo3).

## Usage

### With [Pillow](https://pillow.readthedocs.io/en/stable/)

```py
from io import BytesIO

from PIL import Image
from qoi_rs import encode, decode

image: Image = ...

qoi_bytes: bytes = encode(image.getdata(), width=image.width, height=image.height)

decoded = decode(qoi_bytes)

assert decoded.width == image.width
assert decoded.height == image.height

decoded_image = Image.frombytes(decoded.mode, (decoded.width, decoded.height), decoded.data)
parsed_decoded = Image.open(BytesIO(qoi_bytes))

assert tuple(decoded_image.getdata()) == tuple(parsed_decoded.getdata())
```
