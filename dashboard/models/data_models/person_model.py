from typing import List

from pydantic import Field

from models.custom_model import CustomModel, collection_name


@collection_name("persons")
class Person(CustomModel):
    name: str
    institution: str = None
    faculty: str = None
    department: str = None
    scientific_grade: str = "Licenciado"
    academic_grade: str = "Ninguno"
    orcid: str = None
    emails: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return self.name

    def format(self):
        try:
            name = self.name.split()

            if len(name) > 2:
                last_names = f"{name[-2]}-{name[-1]}"
                names = ".".join([n[0] for n in name[:-2]])
            else:
                last_names = name[-1]
                names = ".".join([n[0] for n in name[:-1]])

            fmt = f"{last_names} {names}"
        except:
            fmt = self.name

        if self.institution == "Universidad de La Habana":
            fmt = f"**{fmt} ({self.faculty})**"

        if self.orcid:
            fmt = f"{fmt} [↩️](https://orcid.org/{self.orcid})"

        return fmt

    @classmethod
    def own(cls):
        return [
            p
            for p in cls.all()
            if p.institution == "Universidad de La Habana" and p.faculty == "MatCom"
        ]
