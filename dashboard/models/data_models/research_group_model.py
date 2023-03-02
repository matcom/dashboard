from __future__ import annotations

from typing import Iterator, List, NamedTuple, Tuple

from models.custom_model import CustomModel, Ref, RefList, collection_name, with_refs
from models.data_models.person_model import Person


class ResearchGroupPersonStatus(NamedTuple):
    is_colaborator: bool
    is_member: bool
    is_head: bool


@with_refs
@collection_name("researchGroups")
class ResearchGroup(CustomModel):
    name: str
    head: Ref[Person] = None
    members: RefList[Person]
    collaborators: RefList[Person]
    keywords: List[str]

    def __str__(self):
        return self.name

    @classmethod
    def from_person(
        cls, person: Person
    ) -> Iterator[Tuple[ResearchGroup, ResearchGroupPersonStatus]]:
        for group in cls.all():
            is_colaborator = person in group.collaborators
            is_member = person in group.members
            is_head = person == group.head
            if is_colaborator or is_member or is_head:
                yield group, ResearchGroupPersonStatus(
                    is_colaborator=is_colaborator, is_member=is_member, is_head=is_head
                )
