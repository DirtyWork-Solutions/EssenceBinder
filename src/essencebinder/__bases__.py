"""
(Abstract) base classes for the EssenceBinder package.

These classes define the fundamental structure and behavior of entities, physical things, abstract concepts, and
their relationships.

**Bases include:**

- **Entity**: Abstract base class for entities in the Essence Binder.
- **Physical**: Abstract base class for physical things.
- **Abstract**: Abstract base class for non-physical entities.
    - **Attributes**: Class for qualities or features that entities can have.
    - **Relations**: Class for connections or associations between entities.
- **Quantities**: Class for numeric or measurable abstractions.
- **Propositions**: Class for statements or pieces of information.

"""

import datetime
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Optional, Union, List
from uuid import uuid4, UUID

from forged.commons.utilities.text import CaseTransformer
from forged.elements.reporting.reported import logger as log

from essencebinder.commons.patterns.decorators import hasmetadata


# CaseTransformer.to_dot_case()

###
#
###

class EssenceBinderBase(ABC):
    pass

class Fundamentals(EssenceBinderBase):
    def __init__(self):
        super().__init__()

class MetaConcepts(EssenceBinderBase):
    def __init__(self):
        super().__init__()

###
#
###

ENTITY_DEF_META = {"object": {
                "uid": None,
                "created_on": None,
                "deleted_on": None,
                "deleted_by": None,
                "is_deleted": False,
                "is_archived": False,
                "archived_on": None,
            },

            "instance": {
                "label": 'unknown',
                "definition": 'unknown',
                "examples": []
            },

            "ontology": {
                "sumo_uri": None,
                "ontology_id": None
            }
        }

@hasmetadata(ENTITY_DEF_META)
class Entity(Fundamentals, ABC):
    """Abstract base class for entities in the Essence Binder."""

    @abstractmethod
    def __init__(self,
                 uid=Optional[Union[str, int, UUID]],
                 label: Optional[str] = None,
                 **kwargs):

        """
        Initialize the entity.

        :param uid: a unique identifier for the entity, can be a *string, int, or UUID*.
        :param args:
        :param kwargs:
        """
        super().__init__()
        self._versions = OrderedDict({
        })
        self._audit = {}

        self.outgoing_relations: List[Relations] = []
        self.incoming_relations: List[Relations] = []

    @property
    def name(self):  # TODO: Rename
        """The name of the entity."""
        return self.__class__.__name__

    @property
    def unique_id(self):
        """The unique identifier of the entity."""
        return self._meta["object"]['uid']

    def set_meta(self, key, value):
        """Set metadata for the entity."""
        self._meta[key] = value

    def get_meta(self, key, group=None):
        """Get metadata for the entity."""
        if group:
            return self._meta[group].get(key)
        return self._meta.get(key)

    def del_meta(self, key, group=None):
        """Delete metadata for the entity."""
        if group:
            del self._meta[group][key]
        else:
            del self._meta[key]

    def add_relation(self, relation):
        """
        Attach a relation to this entity (must be a subject or target).
        :return:
        """
        #
        if relation.subject == self:
            self.outgoing_relations.append(relation)

        if relation.target == self:
            self.incoming_relations.append(relation)

    def remove_relation(self):
        pass

    def get_related_entities(self,
                             relation_type=None,
                             direction='outgoing'):

        if direction == 'any':
            relations = self.outgoing_relations + self.incoming_relations
        elif direction == 'outgoing':
            relations = self.outgoing_relations
        elif direction == 'incoming':
            relations = self.incoming_relations
        else:
            raise ValueError(f"'{direction}' is not a valid direction. Use 'outgoing', 'incoming', or 'any'.")

        return [r.target if direction == 'outgoing' else
                r.subject for r in relations if not relation_type or isinstance(r, relation_type)
                ]

    def has_relation_with(self,
                          other,
                          relation_type=None):
        return any(
            (r.subject == self and r.target == other or r.subject == other and r.target == self)
            and
            (not relation_type or isinstance(r, relation_type))
            for r in self.outgoing_relations + self.incoming_relations
        )


    def is_part_of_recursive(self, target) -> bool:
        """

        :param target:
        :return:
        """
        for relation in self.outgoing_relations:
            #
            if target.__class__.__name__ == 'PartOf':
                if relation.target == target:
                    return True
                if relation.target.is_part_of_recursive(target):
                    return True
                return False



    def __repr__(self):
        """String representation of the entity."""
        return f"{self.__class__.__name__}({self._meta['object']['uid']})"



###
# PHYSICAL
###

class Physical(Entity):
    """Abstract base class for physical things."""

    def __init__(self):
        super().__init__()
        self._meta['physical'] = True  # TODO: Do I want this?

class Objects(Physical):
    """Discrete physical things."""
    def __init__(self):
        super().__init__()


class Processes(Physical):
    """
    Things that occur or unfold over time.
    """
    def __init__(self, duration: Optional[Union[str, int, float]] = None):
        super().__init__()
        self.duration = duration


###
# ABSTRACT
###

class Abstract(Entity):
    """
    Non-physical entities like concepts, properties, etc.
    """
    def __init__(self, metadata: Optional[dict] = None):
        super().__init__()


class Attributes(Abstract):
    """
    Qualities or features that entities can have.
    """
    def __init__(self):
        super().__init__()


class Relations(Abstract):
    """
    Connections or associations between entities.
    """
    def __init__(self,
                 subject: Entity,
                 target: Entity,
                 label: Optional[str] = None,
                 definition: Optional[str] = None,
                 symmetric: bool = False,
                 transitive: bool = False,
                 metadata: Optional[dict] = None):
        super().__init__(metadata)
        self.subject = subject
        self.target = target
        self._meta['object']['label'] = label or 'unknown'
        self.definition = definition or 'unknown'
        self.symmetric = symmetric
        self.transitive = transitive
        log.success(f"Relation '{self._meta['object']['label']}' created between:\n"
                    f"{self.subject.name} ({self.subject.unique_id}) and {self.target.name} ({self.target.unique_id})"
                    f"{' - with weighting of ' if self.is_weighted else ''}{self._weight if self.is_weighted else ''}.")


    @abstractmethod
    def relates(self, *entities: Entity) -> bool:
        pass

    def describe(self, inc_meta: bool = False) -> dict:  # TODO: Optionally include metadata in the return
        if inc_meta:
            log.error("Not Implemented Yet: Including metadata in the describe of Relations.")

        return {  # FIXME: turn to a variable usable in super calls? They can just append
            "label": self._meta['object']['label'],
            "definition": self.definition,
            "subject": self.subject.name,
            "target": self.target.name,
            "symmetric": self._meta['object']['symmetric'],
            "transitive": self._meta['object']['transitive']
        }



    @property
    def is_weighted(self):
        try:
            getattr(self, '_weight')
        except AttributeError:
            log.debug('_weight was not found, assuming no weighting on the relation.')
            return False
        except Exception as e:
            log.error(f'An unexpected error occurred while checking for weighting on the relation: {e}')
        return True


class Quantities(Abstract):
    """
    Numeric or measurable abstractions.

    Significantly leverages the **Pint** library for unit handling.
    """
    def __init__(self, value: Optional[Union[str, int, float]], unit: Optional[str] = None):
        super().__init__()
        self.value = value
        self.unit = unit or 'unknown'

        # Soft checks etc
        if self.unit == 'unknown':
            log.warning(f"Unit is unknown for a '{self.__class__.__name__}' object instance ({self.unique_id}) with value '{self.value}'.")

class Propositions(Abstract):
    """
    Statements or pieces of information (*can be true/false*).
    """
    def __init__(self,
                 content: Optional[str],
                 truth_value: Optional[Union[bool, int, float]] = None,
                 metadata: Optional[dict] = None
                 ):
        super().__init__(metadata=metadata)
        self.content = content or 'unknown'
        self.truth_value = truth_value or 'unknown'

    @property
    def is_true(self):
        return self.truth_value


    def describe(self, inc_meta: bool = False) -> dict:  # TODO: Optionally include metadata in the return
        if inc_meta:
            log.error("Not Implemented Yet: Including metadata in the describe of Relations.")

        return {
            "content": self.content,
            "truth_value": self.truth_value,
        }

class SetOrClass(Fundamentals):  # TODO: Is this needed?
    """Abstract base class for sets or classes in Essence Binder."""

    def __init__(self):
        super().__init__()
