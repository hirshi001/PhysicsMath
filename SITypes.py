import numbers
from enum import Enum, auto
from numbers import Number
from typing import Any


class Dimension(Enum):
    TIME = auto()
    LENGTH = auto()
    MASS = auto()
    CURRENT = auto()

BASE = 10
class Coefficient(Number):
    def __init__(self, coeff: float, exponent: int = 0):

        while abs(coeff) >= BASE:
            coeff /= BASE
            exponent += 1

        while abs(coeff) < 1:
            coeff *= BASE
            exponent -= 1

        self.coeff = coeff
        self.exponent = exponent


    def __add__(self, other):
        if isinstance(other, Coefficient):
            exponent_to_use = max(self.exponent, other.exponent)
            coeff: float
            if self.exponent == exponent_to_use:
                coeff = self.coeff + other.coeff * (BASE ** (other.exponent - self.exponent))
            else:
                coeff = self.coeff * (BASE ** (self.exponent - other.exponent)) + other.coeff
            return Coefficient(coeff, exponent_to_use)


        elif isinstance(other, numbers.Number):
            # convert number to Coefficient
            if other == 0:
                return self
            return self + Coefficient(float(other), 0)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Coefficient(-self.coeff, self.exponent)

    def __pos__(self):
        return self

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Coefficient):
            coeff = self.coeff * other.coeff
            exponent = self.exponent + other.exponent
            return Coefficient(coeff, exponent)

        elif isinstance(other, numbers.Number):
            coeff = float(self.coeff * other)
            exponent = self.exponent
            return Coefficient(coeff, exponent)

        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Coefficient):
            coeff = self.coeff / other.coeff
            exponent = self.exponent - other.exponent
            return Coefficient(coeff, exponent)

        elif isinstance(other, numbers.Number):
            coeff = float(self.coeff / other)
            exponent = self.exponent
            return Coefficient(coeff, exponent)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            coeff = float(other / self.coeff)
            exponent = -self.exponent
            return Coefficient(coeff, exponent)

        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int):
            coeff = self.coeff ** other
            exponent = self.exponent * other
            return Coefficient(coeff, exponent)

        return NotImplemented

    def __rpow__(self, other):
        return NotImplemented

    def __abs__(self):
        return Coefficient(abs(self.coeff), self.exponent)

    def __eq__(self, other):
        if isinstance(other, Coefficient):
            return self.coeff == other.coeff and self.exponent == other.exponent
        elif isinstance(other, numbers.Number):
            return self == Coefficient(float(other), 0)
        return NotImplemented

    def __hash__(self):
        return hash((self.coeff, self.exponent))

    def __str__(self):
        return f"{self.coeff} x {BASE}^{self.exponent}"





prefix_mapping: dict[int, Prefix] = {}


class Prefix:
    def __init__(self, name: str, value: int, symbol: str):
        self.name = name
        self.value = value
        self.symbol = symbol
        prefix_mapping[self.value] = self

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"Prefix(name={self.name}, value={self.value}, symbol={self.symbol})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Prefix):
            return NotImplemented
        return self.name == other.name and self.value == other.value and self.symbol == other.symbol


QUETTA = Prefix("quetta", 30, "Q")
RONNA = Prefix("ronna", 27, "R")
YOTTA = Prefix("yotta", 24, "Y")
ZETTA = Prefix("zetta", 21, "Z")
EXA = Prefix("exa", 18, "E")
PETA = Prefix("peta", 15, "P")
TERA = Prefix("tera", 12, "T")
GIGA = Prefix("giga", 9, "G")
MEGA = Prefix("mega", 6, "M")
KILO = Prefix("kilo", 3, "k")
HECTO = Prefix("hecto", 2, "h")
DECA = Prefix("deca", 1, "da")
UNIT = Prefix("", 0, "")
DECI = Prefix("deci", -1, "d")
CENTI = Prefix("centi", -2, "c")
MILLI = Prefix("milli", -3, "m")
MICRO = Prefix("micro", -6, "µ")
NANO = Prefix("nano", -9, "n")
PICO = Prefix("pico", -12, "p")
FEMTO = Prefix("femto", -15, "f")
ATTO = Prefix("atto", -18, "a")
ZEPTO = Prefix("zepto", -21, "z")
YOCTO = Prefix("yocto", -24, "y")
RONTO = Prefix("ronto", -27, "r")
QUECTO = Prefix("quecto", -30, "q")


class Unit:
    type UnitType = dict[Dimension, int]
    types: UnitType  # This is the precision. Dimensions says what we are meaasuring, Prefix is the magnitude of the smallest unit, int is the exponent of the unit (e.g. m^2 would have exponent 2 for length)

    def __init__(self, types: UnitType):
        if not isinstance(types, dict):
            raise ValueError("types must be a dictionary")
        self.types = types

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        return self.types == other.types

    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        new_types = {si_type: exponent * other for si_type, exponent in self.types.items()}
        return Unit(new_types)

    def __mul__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        new_types = {**self.types}
        for si_type, exponent in other.types.items():
            if si_type not in new_types:
                new_types[si_type] = exponent
            else:
                new_exponent = new_types[si_type] + exponent
                if new_exponent != 0:
                    new_types[si_type] = new_exponent
                else:
                    del new_types[si_type]
        return Unit(new_types)

    def __truediv__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        new_types = {**self.types}
        for si_type, exponent in other.types.items():
            if si_type not in new_types:
                new_types[si_type] = -exponent
            else:
                new_exponent = new_types[si_type] - exponent
                if new_exponent != 0:
                    new_types[si_type] = new_exponent
                else:
                    del new_types[si_type]
        return Unit(new_types)

    def __invert__(self):
        new_types = {si_type: -exponent for si_type, exponent in self.types.items()}
        return Unit(new_types)

    def __str__(self):
        if not self.types:
            return "unitless"
        unit_str = ""
        for dimension, exponent in self.types.items():
            if exponent == 0:
                continue
            unit_str += f"{dimension}"
            if exponent != 1:
                unit_str += f"^{exponent}"
            unit_str += " "
        return unit_str.strip()

    def to_string(self, precisions: dict[Dimension, Prefix]):
        if not self.types:
            return "unitless"
        unit_str = ""
        for dimension, exponent in self.types.items():
            if exponent == 0:
                continue
            name: str = ""
            if dimension in precisions:
                name = precisions[dimension].name
            unit_str += f"{name}{dimension}"
            if exponent != 1:
                unit_str += f"^{exponent}"
            unit_str += " "
        return unit_str.strip()




class Value:
    value: Coefficient
    unit: Unit


    def __init__(self, value: Any[float, int, Coefficient], unit: Unit):
        if not isinstance(unit, Unit):
            raise ValueError("unit must be an instance of Unit")

        if not isinstance(value, Coefficient):
            value = Coefficient(float(value), 0)

        self.value = value
        self.unit = unit

    def __add__(self, other):
        if not isinstance(other, Value):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot add values with different units")
        return Value(self.value + other.value, self.unit)

    def __sub__(self, other):
        if not isinstance(other, Value):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot add values with different units")
        return Value(self.value - other.value, self.unit)

    def __neg__(self):
        return Value(-self.value, self.unit)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Value(self.value * other, self.unit)
        elif isinstance(other, Value):
            new_value = self.value * other.value
            new_unit = self.unit * other.unit
            return Value(new_value, new_unit)
        elif isinstance(other, Prefix):
            new_value = self.value * Coefficient(1, other.value)
            return Value(new_value, self.unit)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Value(self.value / other, self.unit)
        elif isinstance(other, Value):
            new_value = self.value / other.value
            new_unit = self.unit / other.unit
            return Value(new_value, new_unit)
        elif isinstance(other, Prefix):
            new_value = self.value / Coefficient(1, other.value)
            return Value(new_value, self.unit)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Number):
            new_value = other / self.value
            new_unit = ~self.unit
            return Value(new_value, new_unit)
        elif isinstance(other, Prefix):
            new_value = Coefficient(1, other.value) / self.value
            new_unit = ~self.unit
            return Value(new_value, new_unit)
        return NotImplemented

    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        new_value = self.value ** other
        new_unit = self.unit ** other
        return Value(new_value, new_unit)

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __call__(self, number: Any[float, int, Coefficient]):
        return self * number

    def name(self, name: str) -> DerivedUnit:
        return DerivedUnit(self.value, self.unit, name)

    def to_string(self, unit: DerivedUnit):
        if self.unit != unit.unit:
            raise ValueError("Cannot convert to a different unit")

        coefficient_for_derived_unit = unit.get_coefficient_for_derived_unit()
        converted_value = self.value / coefficient_for_derived_unit
        return f"{converted_value} {unit.get_derived_string()}"



class DerivedUnit(Value):
    _names: dict[tuple[Prefix, str], int]# This is a mapping from name to the number of times it has been used. This is used to ensure that we don't have duplicate names for derived units.

    def __init__(self, value: Any[float, int, Coefficient], unit: Unit, name: Any[str, dict[tuple[Prefix, str], int]]):
        super().__init__(value, unit)
        self._names = {}
        if isinstance(name, str):
            self._names[(UNIT, name)] = 1
        else:
            self._names = name

    def __mul__(self, other):
        if isinstance(other, DerivedUnit):
            new_value = self.value * other.value
            new_unit = self.unit * other.unit

            new_names = {**self._names,}
            for name, count in other._names.items():
                if name not in new_names:
                    new_names[name] = count
                else:
                    new_names[name] += count
            return DerivedUnit(new_value, new_unit, new_names)
        else:
            return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, Prefix):
            if len(self._names) != 1:
                raise ValueError("Prefix x DerivedUnit only works if DerivedUnit has only one name")
            (prefix, name), count = next(iter(self._names.items()))
            if prefix != UNIT:
                raise ValueError("Prefix x DerivedUnit only works if DerivedUnit has only one name and that name is not already prefixed")
            new_names = {(other, name): count}
            new_value = self.value * Coefficient(1, other.value)
            return DerivedUnit(new_value, self.unit, new_names)
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, DerivedUnit):
            new_value = self.value / other.value
            new_unit = self.unit / other.unit
            new_names = {**self._names,}
            for name, count in other._names.items():
                if name not in new_names:
                    new_names[name] = -count
                else:
                    new_names[name] -= count
            return DerivedUnit(new_value, new_unit, new_names)
        else:
            return super().__truediv__(other)


    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        if isinstance(other, int):
            new_value = self.value ** other
            new_unit = self.unit ** other
            new_names = {name: count * other for name, count in self._names.items()}
            return DerivedUnit(new_value, new_unit, new_names)
        else:
            return super().__pow__(other)

    def get_coefficient_for_derived_unit(self) -> Coefficient:
        exponent = 0
        for (prefix, name), count in self._names.items():
            if prefix != UNIT:
                exponent += prefix.value * count
        return Coefficient(1, exponent)

    def get_derived_string(self) -> str:
        name_str = ""
        for (prefix, name), count in self._names.items():
            if count == 0:
                continue
            if prefix != UNIT:
                name_str += f"{prefix.name}"
            name_str += f"{name}"
            if count != 1:
                name_str += f"^{count}"
            name_str += " "
        return name_str.strip()



SECOND = DerivedUnit(Coefficient(1), Unit({Dimension.TIME: 1}), "second")
METER = DerivedUnit(Coefficient(1), Unit({Dimension.LENGTH: 1}), "meter")
GRAM = DerivedUnit(Coefficient(1), Unit({Dimension.MASS: 1}), "gram")
AMPERE = DerivedUnit(Coefficient(1), Unit({Dimension.CURRENT: 1}), "ampere")

MILE = (METER * 1609.34).name("mile")
KILOGRAM = KILO * GRAM

NEWTON = (KILOGRAM * METER / (SECOND ** 2)).name("newton")
JOULE = (NEWTON * METER).name("joule")
COULOMB = (AMPERE * SECOND).name("coulomb")
VOLT = (JOULE / COULOMB).name("volt")
FARAD = (COULOMB / VOLT).name("farad")
