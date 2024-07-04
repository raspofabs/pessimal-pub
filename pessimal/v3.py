from dataclasses import dataclass
import math


@dataclass(frozen=True)
class V3:
    x: float
    y: float
    z: float

    def __sub__(self, other):
        assert isinstance(other, V3)
        return V3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        assert isinstance(other, V3)
        return V3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other: float):
        return V3(self.x * other, self.y * other, self.z * other)

    def as_coord(self):
        return int(self.x), int(self.y), int(self.z)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
