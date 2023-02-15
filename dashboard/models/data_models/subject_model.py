from models.custom_model import CustomModel, collection_name


@collection_name("subjects")
class Subject(CustomModel):
    subject: str
    career: str
    semester: int
    year: int

    def __str__(self) -> str:
        return self.subject
