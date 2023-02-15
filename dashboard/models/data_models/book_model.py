from pydantic import HttpUrl

from models.custom_model import with_refs
from models.data_models.publication_model import Publication


@with_refs
class Book(Publication):
    title: str
    publisher: str
    pages: int = None
    url: HttpUrl = None
    isbn: str = None
    edition: int = 1
    year: int = 2022

    def format(self):
        text = [f"📕 {self.title}."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"{self.publisher}, ISBN: {self.isbn}, Edición: {self.edition}, Páginas: {self.pages}."
        )

        return " ".join(text)
