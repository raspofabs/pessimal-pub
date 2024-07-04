from dataclasses import dataclass
from ast import literal_eval
import math


@dataclass(frozen=True)
class V2:
    x: float
    y: float

    @staticmethod
    def parse(string):
        if string is None:
            return V2(0, 0)
        tuple_value = literal_eval(string)
        return V2(*tuple_value)

    def __str__(self):
        return f"[{self.x:.2f}, {self.y:.2f}]"

    def __sub__(self, other):
        assert isinstance(other, V2)
        return V2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        assert isinstance(other, V2)
        return V2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        return V2(self.x * other, self.y * other)

    def __rmul__(self, other: float):
        return V2(self.x * other, self.y * other)

    def __neg__(self):
        return V2(-self.x, -self.y)

    def as_coord(self):
        return int(self.x), int(self.y)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normal(self):
        return self * (1.0 / self.mag())

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def rot90(self):
        return V2(-self.y, self.x)
