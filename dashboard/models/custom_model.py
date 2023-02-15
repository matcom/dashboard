from __future__ import annotations
import logging

import os
from inspect import isclass
from pathlib import Path
from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID, uuid4

import yaml
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic.class_validators import Validator
from typing_extensions import Self

USING_MONGO = os.environ["USE_MONGO"] != ""


ModelT = TypeVar("ModelT", bound="CustomModel")


class Ref(Generic[ModelT]):
    """
    Represents a reference to a custom model.

    A field of type Ref[T] should be treated as a T directly. It will load its
    value in a lazy way. In case of setting a value, it must be also of type T,
    the CustomModel setter will automatically create a Ref[T] using the T's
    UUID.
    """

    def __init__(self, uuid: UUID, model_type: ModelT, cache=None):
        self.uuid = uuid
        self.model_type = model_type
        self.cache: Optional[ModelT] = cache

    def _load_yaml(self) -> ModelT:
        if self.cache is not None:
            return self.cache
        return self.model_type.get(str(self.uuid))

    def load(self) -> ModelT:
        return self._load_yaml()

    def clear_cache(self):
        self.cache = None


class RefList(Generic[ModelT]):
    """
    Represents a reference to a list of custom models.

    A field of type RefList[T] should be treated as a List[T] directly. It will
    load its value in a lazy way. In case of setting a value, it must be also
    of type List[T], the CustomModel setter will automatically create a
    RefList[T] using the T's UUID.
    """

    def __init__(self, uuids: List[UUID], model_type: ModelT, cache=None):
        self.uuids = uuids
        self.model_type = model_type
        self.cache: List[Optional[ModelT]] = (
            [None] * len(uuids) if cache is None else cache
        )

    def clear_cache(self):
        for i in range(len(self.cache)):
            self.cache[i] = None

    def load(self):
        return self._load_yaml()

    def _load_yaml_at(self, idx) -> ModelT:
        cached = self.cache[idx]
        if cached is not None:
            return cached
        val = self.cache[idx] = self.model_type.get(str(self.uuids[idx]))
        return val

    def _load_yaml(self) -> List[ModelT]:
        return [self._load_yaml_at(i) for i in range(len(self.uuids))]


def with_refs(model_class: ModelT) -> ModelT:
    """
    Decorator that adds pydantic validators for all the Ref[T] and RefList[T]
    fields in a CustomModel.
    """
    fields = model_class.__fields__
    for field_name, field in fields.items():
        if isclass(field.type_) and issubclass(field.type_, Ref):
            logging.error(f"Validating {model_class} - {field}")

            # Function that returns a validator for a Ref[T] field
            def _ref_val_wrapper(field):
                def ref_val(cls, value):
                    if value is None or isinstance(value, Ref):
                        return value
                    return Ref(uuid=value.uuid, model_type=field.annotation.__args__[0])

                return ref_val

            model_class.__fields__[field_name].class_validators[field_name] = Validator(
                _ref_val_wrapper(field), pre=True
            )

        elif isclass(field.type_) and issubclass(field.type_, RefList):
            logging.error(f"Validating {model_class} - {field}")

            # Function that returns a validator for a RefList[T] field
            def _reflist_val_wrapper(field):
                def ref_list_val(cls, value):
                    if value is None or isinstance(value, RefList):
                        return value
                    return RefList(
                        uuids=[val.uuid for val in value],
                        model_type=field.annotation.__args__[0],
                    )

                return ref_list_val

            model_class.__fields__[field_name].class_validators[field_name] = Validator(
                _reflist_val_wrapper(field), pre=True
            )
        model_class.__fields__[field_name].populate_validators()
    return model_class


class CustomModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    uuid: UUID = Field(default_factory=uuid4)

    def __getattribute__(self, name: str) -> Any:
        # If dundler method return default
        if name.startswith("__"):
            return super().__getattribute__(name)

        # Check is asking for ref directly
        return_ref = name.endswith("_ref")
        if return_ref:
            # If so, fix the attr name to the correct field name
            name = name[:-4]

        model_field = self.__class__.__fields__.get(name, None)
        if model_field is not None:
            is_ref_field = isclass(model_field.type_) and issubclass(
                model_field.type_, (Ref, RefList)
            )
            if is_ref_field and not return_ref:
                ref = super().__getattribute__(name)
                return None if ref is None else ref.load()

        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if value is None:
            return super().__setattr__(name, value)

        model_field = self.__class__.__fields__.get(name, None)
        if model_field is not None:
            # Create a Ref or a RefList if field is a ref.
            if isclass(model_field.type_) and issubclass(model_field.type_, Ref):
                assert isinstance(
                    value, CustomModel
                ), "Only custom models can be assigned to Ref fields"

                model_type = model_field.annotation.__args__[0]
                return super().__setattr__(
                    name,
                    Ref(uuid=value.uuid, model_type=model_type, cache=value),
                )
            if isclass(model_field.type_) and issubclass(model_field.type_, RefList):
                assert isinstance(
                    value, list
                ), "Only lists can be assigned to RefList fields"
                assert all(
                    isinstance(val, CustomModel) for val in value
                ), "All elements in the list must be custom models"

                model_type = model_field.annotation.__args__[0]
                ref = RefList(
                    uuids=[val.uuid for val in value],
                    model_type=model_type,
                    cache=value,
                )
                return super().__setattr__(name, ref)

        return super().__setattr__(name, value)

    def check(self):
        return True

    def yaml(self) -> str:
        return yaml.dump(self.encode(), allow_unicode=True)

    def encode(self) -> dict:
        _dict = self.dict()

        # Check for ref fields and replace them by their id (or id list).
        result = {}
        for key, value in _dict.items():
            if isinstance(value, Ref):
                result[key] = value.uuid
            elif isinstance(value, RefList):
                result[key] = value.uuids
        _dict.update(result)

        data = jsonable_encoder(_dict)
        result = {}

        for key, value in data.items():
            if isinstance(value, dict) and "uuid" in value:
                result[key] = value["uuid"]
            elif isinstance(value, list) and all(
                [isinstance(v, dict) and "uuid" in v for v in value]
            ):
                result[key] = [v["uuid"] for v in value]
            elif isinstance(value, HttpUrl):
                result[key] = str(value)
            else:
                result[key] = value

        return result

    def _encode(self, v):
        if isinstance(v, (int, float, str)):
            return v
        if isinstance(v, list):
            return [self._encode(vi) for vi in v]
        if isinstance(v, dict):
            return {ki: self._encode(vi) for ki, vi in v.items()}

        return str(v)

    def save(self):
        path: Path = (
            Path("/src/data") / self.__class__.__name__ / (str(self.uuid) + ".yaml")
        )
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("w") as fp:
            fp.write(self.yaml())

    @classmethod
    def all(cls) -> List[Self]:
        path: Path = Path("/src/data") / cls.__name__
        items = []

        for fname in path.glob("*.yaml"):
            with open(fname, encoding="utf-8") as fp:
                items.append(cls.load(fp))

        return items

    @classmethod
    def find(cls, **kwargs):
        for item in cls.all():
            if all(getattr(item, k, None) == v for k, v in kwargs.items()):
                return item

        raise KeyError(str(kwargs))

    @classmethod
    def get(cls, uuid: str) -> Self:
        path: Path = Path("/src/data") / cls.__name__ / (str(uuid) + ".yaml")

        with path.open() as fp:
            return cls.load(fp)

    @classmethod
    def load(cls, fp) -> Self:
        data = yaml.safe_load(fp)
        values = {}

        for key, value in data.items():
            field = cls.__fields__[key]

            if isclass(field.type_) and issubclass(field.type_, Ref):
                value = Ref(uuid=UUID(value), model_type=field.annotation.__args__[0])

            if isclass(field.type_) and issubclass(field.type_, RefList):
                assert isinstance(value, list)
                value = RefList(
                    uuids=[UUID(val) for val in value],
                    model_type=field.annotation.__args__[0],
                )

            values[key] = value

        logging.error(f"Loading {data}")
        return cls(**values)

    def __hash__(self):
        return hash(str(self.uuid))

    def __eq__(self, other):
        return isinstance(other, CustomModel) and self.uuid == other.uuid
