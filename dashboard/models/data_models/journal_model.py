from typing import List

from pydantic import Field, HttpUrl

from models.custom_model import CustomModel, collection_name


@collection_name("journals")
class Journal(CustomModel):
    title: str
    publisher: str
    issn: str = ""
    indices: List[str] = Field(default_factory=list)
    url: HttpUrl = None

    def save(self):
        func_check_same_data = (
            lambda c: self.title == c.title and self.publisher == c.publisher
        )
        class_with_same_data = next(filter(func_check_same_data, Journal.all()), None)
        if class_with_same_data:
            self.uuid = class_with_same_data.uuid
        CustomModel.save(self)

    def format(self):
        indices = ", ".join(f"_{index}_" for index in self.indices)
        title = f"**{self.title}**"

        if self.url:
            title = f"[{title}]({self.url})"

        return (
            f"🗞️ {title}, {self.publisher}. ISSN: {self.issn}. Indexado en: {indices}."
        )

    def __str__(self):
        return f"{self.title} ({self.publisher})"
