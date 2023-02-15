from typing import List

from models.custom_model import CustomModel, RefList, with_refs
from models.data_models.person_model import Person


@with_refs
class Publication(CustomModel):
    authors: RefList[Person]

    @classmethod
    def from_authors(cls, authors: List[Person]):
        authors = set(authors)

        for item in cls.all():
            if set(item.authors) & authors:
                yield item
