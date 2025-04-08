import pytest
from src.essencebinder.__bases__ import (
    Entity, Physical, Objects, Processes, Abstract, Attributes, Relations,
    Quantities, Propositions, SetOrClass, SubclassSubrelation, Instances,
    Disjointness, Ranges, Parts
)
from uuid import UUID

from essencebinder.things.abstract.relation.relationships import (
    PartOf, CompatibleWith, HasRole, relate
)
from essencebinder.__bases__ import Entity


class ConcreteEntity(Entity):
    def __init__(self, uid=None):
        super().__init__(uid=uid)
        self.parts = []
        self.compatible = []
        self.roles = []

    def __repr__(self):
        return f"TestEntity({self.unique_id})"

    """
        def __repr__(self):
        return f"Entity({self.unique_id})
        """


def test_part_of_relationship():
    subject = ConcreteEntity(uid="123")
    target = ConcreteEntity(uid="456")
    target.parts.append(subject)

    relation = PartOf(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'part of'


def test_compatible_with_relationship():
    subject = ConcreteEntity(uid="123")
    target = ConcreteEntity(uid="456")
    target.compatible.append(subject)

    relation = CompatibleWith(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'compatible with'


def test_has_role_relationship():
    subject = ConcreteEntity(uid="123")
    target = ConcreteEntity(uid="456")
    target.roles.append(subject)

    relation = HasRole(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'has role'


def test_relate_function():
    subject = ConcreteEntity(uid="123")
    target = ConcreteEntity(uid="456")

    relate(subject, PartOf, target)
    assert len(subject.outgoing_relations) == 1
    assert len(target.incoming_relations) == 1
    assert isinstance(subject.outgoing_relations[0], PartOf)
    assert isinstance(target.incoming_relations[0], PartOf)
    assert subject.outgoing_relations[0].target == target
    assert target.incoming_relations[0].subject == subject



def test_entity_initialization():
    entity = ConcreteEntity(uid="12345")
    assert entity.unique_id == "12345"
    assert entity.get_meta("uid", "object") == "12345"
    assert entity.get_meta("created_on", "object") is not None


def test_entity_meta_operations():
    entity = ConcreteEntity()
    entity.set_meta("test_key", "test_value")
    assert entity.get_meta("test_key") == "test_value"
    entity.del_meta("test_key")
    assert entity.get_meta("test_key") is None


def test_entity_repr():
    entity = ConcreteEntity(uid="12345")
    assert repr(entity) == "Entity(12345)"


def test_physical_initialization():
    physical = Physical()
    assert physical.get_meta("physical") is True


def test_objects_initialization():
    obj = Objects()
    assert obj.get_meta("physical") is True


def test_processes_initialization():
    process = Processes()
    assert process.get_meta("physical") is True


def test_abstract_initialization():
    abstract = Abstract()
    assert abstract.get_meta("physical") is None


def test_attributes_initialization():
    attributes = Attributes()
    assert attributes.get_meta("physical") is None


def test_relations_initialization():
    relations = Relations()
    assert relations.get_meta("physical") is None


def test_quantities_initialization():
    quantities = Quantities()
    assert quantities.get_meta("physical") is None


def test_propositions_initialization():
    propositions = Propositions()
    assert propositions.get_meta("physical") is None


def test_set_or_class_initialization():
    set_or_class = SetOrClass()
    assert isinstance(set_or_class, SetOrClass)


def test_metaconcepts_initialization():
    subclass_subrelation = SubclassSubrelation()
    instances = Instances()
    disjointness = Disjointness()
    ranges = Ranges()
    parts = Parts()

    assert isinstance(subclass_subrelation, SubclassSubrelation)
    assert isinstance(instances, Instances)
    assert isinstance(disjointness, Disjointness)
    assert isinstance(ranges, Ranges)
    assert isinstance(parts, Parts)