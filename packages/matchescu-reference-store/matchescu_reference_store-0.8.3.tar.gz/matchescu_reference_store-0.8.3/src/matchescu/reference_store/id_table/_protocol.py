from collections.abc import Iterable
from typing import Protocol, Sized

from matchescu.typing import EntityReferenceIdentifier, EntityReference


class IdTable(Iterable[EntityReference], Sized, Protocol):
    def get(self, ref_id: EntityReferenceIdentifier) -> EntityReference:
        pass

    def get_all(
        self, ref_ids: Iterable[EntityReferenceIdentifier]
    ) -> Iterable[EntityReference]:
        pass

    def get_by_source(self, source: str) -> Iterable[EntityReference]:
        pass

    def put(self, ref: EntityReference) -> None:
        pass
