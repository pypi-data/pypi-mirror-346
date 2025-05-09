from typing import Protocol, Iterable, Sized

from matchescu.typing import EntityReferenceIdentifier


class BinaryComparisonSpace(
    Iterable[tuple[EntityReferenceIdentifier, EntityReferenceIdentifier]],
    Sized,
    Protocol,
):
    def put(
        self, left: EntityReferenceIdentifier, right: EntityReferenceIdentifier
    ) -> None:
        pass
