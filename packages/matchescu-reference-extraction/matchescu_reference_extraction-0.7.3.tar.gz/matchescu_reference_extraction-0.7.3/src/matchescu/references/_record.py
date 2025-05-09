import itertools
from collections.abc import Iterable

from matchescu.data import Record
from matchescu.typing import EntityReferenceIdentifier


class EntityReference(Record):
    id: EntityReferenceIdentifier

    def __init__(self, identifier: EntityReferenceIdentifier, value: Iterable):
        super().__init__(value)
        self.id = identifier

    def __eq__(self, __value):
        if not isinstance(__value, EntityReference):
            return False
        return __value.id == self.id

    def __ne__(self, __value):
        return not self.__eq__(__value)

    def __repr__(self):
        return "EntityReference(id={})".format(repr(self.id))

    def __hash__(self):
        return hash(self.id)

    def __dir__(self):
        return list(itertools.chain(super().__dir__(), self._attr_names.keys()))

    def as_dict(self) -> dict:
        return {
            attr_name: self._attr_values[attr_idx]
            for attr_name, attr_idx in self._attr_names.items()
        }
