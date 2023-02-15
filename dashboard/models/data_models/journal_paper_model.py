from pydantic import HttpUrl

from models.custom_model import Ref, with_refs
from models.data_models.journal_model import Journal
from models.data_models.person_model import Person
from models.data_models.publication_model import Publication


@with_refs
class JournalPaper(Publication):
    title: str
    corresponding_author: Ref[Person] = None
    url: HttpUrl = None
    journal: Ref[Journal] = None
    issue: int = 1
    volume: int = 1
    year: int = 2022
    balance: int = 2022

    def format(self):
        text = [f"📃 {self.title}."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"En _{self.journal.title}_, {self.journal.publisher}. ISSN: {self.journal.issn}."
        )
        text.append(f"Volumen {self.volume}, Número {self.issue}, {self.year}.")
        return " ".join(text)
