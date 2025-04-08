from essencebinder.__bases__ import Relations, Entity
from essencebinder.commons.patterns.mixins import HasWeightMixin as HasWeight


class PartOf(Relations):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Indicates the subject is a part of the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'part of'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])


class CompatibleWith(Relations, HasWeight):  # FIXME: Fails testing
    def __init__(self,
                 subject,
                 target,
                 definition: str = 'Subject is functionally or structurally compatible with the target.'):
        super().__init__(subject, target, definition)
        self._meta['object']['label'] = 'compatible with'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.subject, "compatible", [])


class HasRole(Relations):  # FIXME: Fails testing
    def __init__(self,
                 subject,
                 target,
                 definition: str = 'Indicates a role played by an entity in a context.'):
        super().__init__(subject, target, definition)
        self._meta['object']['label'] = 'has role'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.subject, "roles", [])


class Location(Relations):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Spatial or temporal location of the subject in relation to the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'located in'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])


class ConnectedTo(Relations, HasWeight):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Indicates the subject is a part of the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'part of'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])


class InstanceOf(Relations):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Indicates the subject is a part of the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'part of'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])

class Performs(Relations):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Indicates the subject is a part of the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'part of'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])

class Causes(Relations, HasWeight):  # TODO: Dunder methods

    def __init__(self,
                 subject:
                 Entity, target: Entity,
                 definition: str = 'Indicates the subject is a part of the target.'
                 ):
        super().__init__(subject, target, definition)

        self._meta['object']['label'] = 'part of'

    def relates(self, *entities: Entity) -> bool:
        return self.subject in getattr(self.target, "parts", [])

###
# Functions & Utilities
###

def relate(subject: Entity,
           relation_cls: type,
           target: Entity,
           **kwargs):
    """

    :param subject:
    :param relation_cls:
    :param target:
    :param kwargs:
    :return:
    """

    relation = relation_cls(subject, target, **kwargs)
    subject.add_relation(relation)
    target.add_relation(relation)


def add_weighting(subject: Entity,  # TODO: Make this actually work better
                  relation_cls: type,
                  target: Entity,
                  weighting: int | float = 1,
                  **kwargs):
    """
    :param subject:
    :param relation_cls:
    :param target:
    :param weighting:
    :param kwargs:
    :return:
    """

    relation = relation_cls(subject, target, **kwargs)
    subject.add_relation(relation)
    target.add_relation(relation)

    if hasattr(subject, "set_weight"):
        subject.set_weight(weighting)

    if hasattr(target, "set_weight"):
        target.set_weight(weighting)