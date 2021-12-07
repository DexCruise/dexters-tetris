from dataclasses import dataclass
from typing import Union


@dataclass
class vector2:
    x: Union[int, float]
    y: Union[int, float]