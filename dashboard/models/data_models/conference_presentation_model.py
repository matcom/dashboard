from models.custom_model import collection_name, with_refs
from models.data_models.publication_model import Publication
from pydantic import HttpUrl


@with_refs
@collection_name("conferencePresentations")
class ConferencePresentation(Publication):
    title: str
    url: HttpUrl = None
    venue: str = None

    location: str = None
    year: int = 2022
    paper: bool = False
    balance: int = 2022
    event_type: str = "Internacional"

    def format(self):
        if self.paper:
            text = ["📃"]
        else:
            text = ["📢"]

        text.append(f"_{self.title}_.")

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(f"En _{self.venue}_, {self.location}, {self.year}")

        return " ".join(text)
