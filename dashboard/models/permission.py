import enum
from functools import reduce
from typing import List

from models.custom_model import CustomModel, Ref, RefList, collection_name, with_refs
from models.data_models.person_model import Person

READ = 1
WRITE = 2
ADMIN = 4

PERMISSIONS = {READ: "Lectura", WRITE: "Escritura", ADMIN: "Administrador"}

PERMISSIONS_BY_NAME = {v: k for k, v in PERMISSIONS.items()}
ALL_PERMISSIONS = reduce(lambda p1, p2: p1 | p2, PERMISSIONS.keys())


@with_refs
@collection_name("permissions")
class Permission(CustomModel):
    section: str
    person: Ref[Person]
    permission: int

    @property
    def can_read(self):
        return Permission.has_read_perm(self.permission)

    @property
    def can_write(self):
        return Permission.has_write_perm(self.permission)

    @staticmethod
    def has_read_perm(permission: int):
        return permission & READ == READ

    @staticmethod
    def has_write_perm(permission: int):
        return permission & WRITE == WRITE

    @staticmethod
    def has_admin_perm(permission: int):
        return permission & ADMIN == ADMIN

    @staticmethod
    def from_list(permissions: List[int]) -> int:
        return reduce(lambda p1, p2: p1 | p2, permissions)

    @staticmethod
    def from_number(permissions: int) -> List[int]:
        return [perm for perm in PERMISSIONS.keys() if permissions & perm == perm]


@with_refs
class ControlledSection(CustomModel):
    permissions: RefList[Permission]
    default: int

    def user_can_read(self, person: Person) -> bool:
        for perm in self.permissions:
            if person.uuid == perm.person_ref.uuid:
                return perm.can_read
        return self.default & READ == READ

    def user_can_write(self, person: Person) -> bool:
        for perm in self.permissions:
            if person.uuid == perm.person_ref.uuid:
                return perm.can_write
        return self.default & WRITE == WRITE
