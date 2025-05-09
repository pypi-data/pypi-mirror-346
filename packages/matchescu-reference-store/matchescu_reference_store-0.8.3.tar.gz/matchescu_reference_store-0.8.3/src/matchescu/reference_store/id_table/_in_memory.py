from functools import partial
from typing import Iterable

from matchescu.reference_store._exceptions import EntityReferenceNotFound
from matchescu.typing import EntityReference, EntityReferenceIdentifier


class InMemoryIdTable(object):
    def __init__(self):
        self._id_table = {}

    def __len__(self) -> int:
        return len(self._id_table)

    def __iter__(self) -> Iterable[EntityReference]:
        return iter(self._id_table.values())

    def put(self, ref: EntityReference) -> None:
        if ref is None:
            return
        self._id_table[ref.id] = ref

    def get(self, ref_id: EntityReferenceIdentifier) -> EntityReference:
        if ref_id not in self._id_table:
            raise EntityReferenceNotFound(ref_id)
        return self._id_table[ref_id]

    def get_all(
        self, ref_ids: Iterable[EntityReferenceIdentifier]
    ) -> Iterable[EntityReference]:
        return list(map(self.get, ref_ids))

    @staticmethod
    def __has_source(identifier: EntityReferenceIdentifier, source: str) -> bool:
        return identifier.source == source

    def get_by_source(self, source: str) -> Iterable[EntityReference]:
        has_source = partial(self.__has_source, source=source)
        ids_with_source = filter(has_source, self._id_table.keys())
        return map(self._id_table.get, ids_with_source)
