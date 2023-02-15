from pathlib import Path
from typing import List

from models.custom_model import CustomModel, collection_name
from models.data_models.person_model import Person


@collection_name("theses")
class Thesis(CustomModel):
    title: str
    authors: List[str]
    advisors: List[str]
    keywords: List[str]
    version: int = 0
    balance: int = 2022

    @classmethod
    def from_advisors(cls, advisors: List[Person]):
        names = set([a.name for a in advisors])

        for thesis in cls.all():
            if set(thesis.advisors) & names:
                yield thesis

    def check(self):
        if not self.title:
            raise ValueError("El título no puede ser vacío.")

        if len(self.authors) == 0:
            raise ValueError("Debe tener al menos un autor.")

        if len(self.advisors) == 0:
            raise ValueError("Debe tener al menos un tutor.")

        if len(self.keywords) < 3:
            raise ValueError("Debe tener al menos 3 palabras clave.")

        return True

    def save_thesis_pdf(self, pdf):
        self.version += 1
        name_pdf = f"{self.uuid}_v{self.version}.pdf"
        path: Path = Path(f"/src/data/Thesis/files/{name_pdf}")
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("wb") as f:
            f.write(pdf.getbuffer())
