import json

from cp_request import Attribute, NamedEntity, Unit, Value
from cp_request.named_entity import NamedEntityEncoder, NamedEntityDecoder


class TestNamedEntity:

    def test_entity(self):
        e1 = NamedEntity(name="one", reference="http://one.one")
        e2 = NamedEntity(name="one", reference="http://one.one")
        assert e1 == e2
        assert e1 != {}

        assert repr(e1) == "NamedEntity(name='one', reference='http://one.one')"
        assert str(e1) == "NamedEntity(name='one', reference='http://one.one')"

    def test_serialization(self):
        e1 = NamedEntity(name="one", reference="http://one.one")
        e_json = json.dumps(e1, cls=NamedEntityEncoder)
        e2 = json.loads(e_json, cls=NamedEntityDecoder)
        assert e1 == e2

    def test_entity_attributes(self):
        concentration = Attribute.create_from(
            name='concentration',
            value=Value(
                value=0.25,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'
                )
            ))
        e1 = NamedEntity(
            name="one",
            reference="http://one.one",
            attributes=[concentration])
        assert e1.is_bound()

        e2 = NamedEntity(
            name="one",
            reference="http://one.one",
            attributes=[concentration])
        assert e1 == e1
        assert e1 == e2
        assert e1 != {}

        assert repr(
            e1) == "NamedEntity(name='one', reference='http://one.one', attributes=[BoundAttribute(name='concentration', value=Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])"
        assert str(
            e1) == "NamedEntity(name='one', reference='http://one.one', attributes=[BoundAttribute(name='concentration', value=Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])"

    def test_entity_attribute_serialization(self):
        concentration = Attribute.create_from(
            name='concentration',
            value=Value(
                value=0.25,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'
                )
            ))
        e1 = NamedEntity(
            name="one",
            reference="http://one.one",
            attributes=[concentration])
        e_json = json.dumps(e1, cls=NamedEntityEncoder)
        e2 = json.loads(e_json, cls=NamedEntityDecoder)
        assert e1 == e2

    def test_entity_unbound_attributes(self):
        concentration = Attribute.create_from(
            name='concentration',
            value=Value(
                value=0.25,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'
                )
            ))
        timepoint = Attribute.create_from(
            name='timepoint',
            unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027')
        )

        e1 = NamedEntity(
            name="one",
            reference="http://one.one",
            attributes=[concentration, timepoint])
        assert not e1.is_bound()
