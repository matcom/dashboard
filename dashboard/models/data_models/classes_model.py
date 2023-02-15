from typing import List
from models.custom_model import CustomModel, Ref, with_refs
from models.data_models.person_model import Person
from models.data_models.subject_model import Subject


@with_refs
class Classes(CustomModel):
    subject: Ref[Subject]
    professor: Ref[Person]
    lecture_hours: int
    practice_hours: int

    @classmethod
    def from_professors(cls, professors: List[Person]):
        for _class in cls.all():
            if _class.professor in professors:
                yield _class

    def save(self):
        func_check_same_data = (
            lambda c: self.subject == c.subject and self.professor == c.professor
        )
        class_with_same_data = next(filter(func_check_same_data, Classes.all()), None)
        if class_with_same_data:
            self.uuid = class_with_same_data.uuid
        CustomModel.save(self)
