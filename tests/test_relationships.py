import pytest
from essencebinder.things.abstract.relation.relationships import (
    PartOf, CompatibleWith, HasRole, relate
)
from essencebinder.__bases__ import Entity


class TestEntity(Entity):
    def __init__(self, uid=None):
        super().__init__(uid=uid)
        self.parts = []
        self.compatible = []
        self.roles = []

    def __repr__(self):
        return f"TestEntity({self.unique_id})"


def test_part_of_relationship():
    subject = TestEntity(uid="123")
    target = TestEntity(uid="456")
    target.parts.append(subject)

    relation = PartOf(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'part of'


def test_compatible_with_relationship():
    subject = TestEntity(uid="123")
    target = TestEntity(uid="456")
    subject.compatible.append(target)

    relation = CompatibleWith(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'compatible with'


def test_has_role_relationship():
    subject = TestEntity(uid="123")
    target = TestEntity(uid="456")
    subject.roles.append(target)

    relation = HasRole(subject, target)
    assert relation.relates(subject, target) is True
    assert relation.subject == subject
    assert relation.target == target
    assert relation._meta['object']['label'] == 'has role'


def test_relate_function():
    subject = TestEntity(uid="123")
    target = TestEntity(uid="456")

    relate(subject, PartOf, target)
    assert len(subject.outgoing_relations) == 1
    assert len(target.incoming_relations) == 1
    assert isinstance(subject.outgoing_relations[0], PartOf)
    assert isinstance(target.incoming_relations[0], PartOf)
    assert subject.outgoing_relations[0].target == target
    assert target.incoming_relations[0].subject == subject