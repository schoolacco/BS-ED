from __future__ import annotations
from typing import Optional
import math
import sys
class Mantissa:
    '''Abstract representation of extremely large numbers.
    Parameters:
    ------------
    Mantissa: Numerical value
    Exponent: Value of exponent as a power of 10
    '''
    def __init__(self, mantissa: int|float, exponent: int|float) -> Mantissa:
        self.num = mantissa
        self.exp = exponent
    def __mul__(a: int|float|Mantissa, b: int|float|Mantissa) -> Mantissa:
      # a and b are (mantissa, exponent) tuples
      if isinstance(a, (int,float)):
          a = Mantissa.float_to_mantissa(a)
      if isinstance(b, (int,float)):
          b = Mantissa.float_to_mantissa(b)
      new_mantissa = a.num * b.num
      new_exponent = a.exp + b.exp
      
      # Normalize if mantissa >= 10
      while new_mantissa >= 10:
          new_mantissa /= 10
          new_exponent += 1
      return Mantissa(new_mantissa, new_exponent)
    def __add__(a: int|float|Mantissa, b: int|float|Mantissa) -> Mantissa:
      # Ensure a has the bigger exponent
      if isinstance(a, (int,float)):
          a = Mantissa.float_to_mantissa(a)
      if isinstance(b, (int,float)):
          b = Mantissa.float_to_mantissa(b)
      if a.exp < b.exp:
          a, b = b, a  # swap references, do not mutate
  
      diff = a.exp - b.exp
      if diff > 300:  # treat b as negligible
          return Mantissa(a.num, a.exp)
  
      # Safe addition for reasonably close exponents
      new_mantissa = a.num + b.num * 10**-diff
      while new_mantissa >= 10:
        new_mantissa /= 10
        a.exp += 1
      return Mantissa(new_mantissa, a.exp)
    def __iadd__(a: int|float|Mantissa, b: int|float|Mantissa) -> Mantissa:
        total = a + b
        return total
    def __round__(self: Mantissa, ndigits: Optional[int]=None) -> Mantissa:
        self.num = round(self.num, ndigits)
        return self
    def __ge__(self: Mantissa, other: int|float|Mantissa) -> bool:
        if other == math.inf: return False
        if isinstance(self, (int, float)):
            self = Mantissa.float_to_mantissa(self)
        if isinstance(other, (int, float)):
            other = Mantissa.float_to_mantissa(other)
        return True if self.exp > other.exp else True if self.exp == other.exp and self.num >= other.num else False
    def __sub__(a: int|float|Mantissa,b: int|float|Mantissa) -> Mantissa:
        if isinstance(a, (int,float)):
          a = Mantissa.float_to_mantissa(a)
        if isinstance(b, (int,float)):
          b = Mantissa.float_to_mantissa(b)
        b.num = -b.num
        return a + b
    def __truediv__(a: int|float|Mantissa,b: int|float|Mantissa) -> Mantissa:
        if isinstance(a, (int,float)):
          a = Mantissa.float_to_mantissa(a)
        if isinstance(b, (int,float)):
          b = Mantissa.float_to_mantissa(b)
        mantissa = a.num/b.num
        exp = a.exp-b.exp
        while mantissa <= 1:
            mantissa*= 10
            exp -= 1
        return Mantissa(mantissa, exp)
    def __lt__(self: Mantissa, other: int|float|Mantissa) -> bool:
        return not self >= other
    def __gt__(self: Mantissa, other: int|float|Mantissa) -> bool:
        return not self <= other
    def __le__(self: Mantissa, other: int|float|Mantissa) -> bool:
        if other == math.inf: return True
        if isinstance(self, (int, float)):
            self = Mantissa.float_to_mantissa(self)
        if isinstance(other, (int, float)):
            other = Mantissa.float_to_mantissa(other)
        return True if self.exp < other.exp else True if self.exp == other.exp and self.num <= other.num else False
    def __float__(self) -> float:
        if self.exp < 308:
            return self.num * (10 ** self.exp)
        else:
            return math.inf
    def __int__(self) -> int:
        if float(self) < sys.maxsize:
            return int(self.num * (10** self.exp))
        else:
            return sys.maxsize
    def to_string(self: Mantissa) -> str:
       return f"{self.num:.2f}e+{self.exp}"
    def to_dict(self: Mantissa) -> dict:
        return {"__mantissa__": True, "number": self.num, "exponent": self.exp}
    @classmethod
    def from_string(cls, string: str) -> Mantissa:
        segments = string.split("e")
        segments = [i.strip("+") for i in segments]
        for segment in segments:
            try:
                segments.remove(segment)
                segments.append(int(round(float(segment))))
            except ValueError:
                return None #Invalid input
        if len(segments) != 2:
            return None #Invalid input
        return cls(segments[1], int(segments[0]))
    @classmethod
    def from_dict(cls, data: dict) -> Mantissa:
        return cls(data["number"], data["exponent"])
    def to_float(self: Mantissa) -> float | Mantissa:
        """Convert the Mantissa to a regular float. If the exponent is too large then return the mantissa"""
        value =  self.num * (10 ** self.exp) if self.exp < 300 else self
        return value
    @staticmethod
    def float_to_mantissa(value: float) -> Mantissa:
      """Converts a float or int into a Mantissa."""
      if isinstance(value, Mantissa):
          return value
      if value == 0:
          return Mantissa(0, 0)
      exponent = int(math.floor(math.log10(abs(value))))
      mantissa = value / (10 ** exponent)
      return Mantissa(mantissa, exponent)