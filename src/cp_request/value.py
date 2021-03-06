import json
from cp_request import Unit, UnitEncoder, UnitDecoder
from typing import Union


class Value:
    """
    Represents a numeric value with a unit.

    JSON serialization provided by {ValueEncoder}, and deserialization by
    {ValueDecoder}.
    """

    def __init__(self, *, value: Union[int, float], unit: Unit):
        self.__value = value
        self.__unit = unit

    def __repr__(self):
        return "Value(value={}, unit={})".format(
            self.value, repr(self.unit))

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value and self.unit == other.unit

    def apply(self, visitor):
        visitor.visit_value(self)

    @property
    def value(self):
        return self.__value

    @property
    def unit(self):
        return self.__unit


class ValueEncoder(json.JSONEncoder):
    """
    A JSONEncoder for the {Value} class.
    """

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Value):
            rep = dict()
            rep['object_type'] = 'value'
            rep['value'] = obj.value
            rep['unit'] = UnitEncoder().default(obj.unit)
            return rep
        return super().default(obj)


class ValueDecoder(json.JSONDecoder):
    """
    A JSONDecoder for the {Value} class.

    Note: the convert method is the object_hook.
    """

    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'value':
            return d
        if 'value' not in d:
            return d
        if 'unit' not in d:
            return d
        return Value(
            value=d['value'],
            unit=UnitDecoder().object_hook(d['unit']))
