import json
from cp_request import Attribute, AttributeEncoder, AttributeDecoder
from typing import List


class NamedEntity:
    """
    Represents an entity in an experiment that has a name,
    a definition reference, and possibly a set of attributes.
    """

    def __init__(self, *, name: str, reference: str,
                 attributes: List[Attribute] = list()):
        self.__name = name
        self.__reference = reference
        self.__attributes = list(attributes)

    def __repr__(self):
        if self.__attributes:
            return "NamedEntity(name={}, reference={}, attributes={})".format(
                repr(self.__name),
                repr(self.__reference),
                repr(self.__attributes))
        return "NamedEntity(name={}, reference={})".format(
            repr(self.__name), repr(self.__reference))

    def __eq__(self, other):
        if not isinstance(other, NamedEntity):
            return False
        return (self.__name == other.__name
                and self.__reference == other.__reference
                and self.__attributes == other.__attributes)

    def apply(self, visitor):
        visitor.visit_named_entity(self)

    @property
    def name(self):
        return self.__name

    @property
    def reference(self):
        return self.__reference

    @property
    def attributes(self):
        return self.__attributes

    def is_bound(self):
        """
        An entity is bound if no attached attribute is not bound.
        """
        for attribute in self.attributes:
            if not attribute.is_bound():
                return False
        return True


class NamedEntityEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, NamedEntity):
            rep = dict()
            rep['object_type'] = 'named_entity'
            rep['name'] = obj.name
            rep['reference'] = obj.reference
            if obj.attributes:
                rep['attributes'] = [
                    AttributeEncoder().default(attr)
                    for attr in obj.attributes
                ]
            return rep
        return super().default(obj)


class NamedEntityDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'named_entity':
            return d
        if 'name' not in d:
            return d
        if 'reference' not in d:
            return d

        attributes = list()
        if 'attributes' in d:
            attributes = [AttributeDecoder().convert(attr_obj)
                          for attr_obj in d['attributes']]

        return NamedEntity(
            name=d['name'],
            reference=d['reference'],
            attributes=attributes
        )
