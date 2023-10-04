from models.custom_model import collection_name, with_refs
from models.data_models.book_model import Book


@with_refs
@collection_name("bookChapters")
class BookChapter(Book):
    chapter: str

    def format(self):
        text = [f"📑 _{self.chapter}_."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"**Capítulo en el libro:** {self.title}, {self.publisher}, ISBN: {self.isbn}, Edición: {self.edition}, Páginas: {self.pages}."
        )

        return " ".join(text)
