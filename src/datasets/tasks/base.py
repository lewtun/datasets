import abc
import dataclasses
from dataclasses import dataclass
from typing import ClassVar, Dict, Type, TypeVar

from ..features import Features


T = TypeVar("T", bound="TaskTemplate")


@dataclass(frozen=True)
class TaskTemplate(abc.ABC):
    task: ClassVar[str]
    input_schema: ClassVar[Features]
    label_schema: ClassVar[Features]

    @property
    def features(self) -> Features:
        return Features(**self.input_schema, **self.label_schema)

    @property
    @abc.abstractmethod
    def column_mapping(self) -> Dict[str, str]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls: Type[T], template_dict: dict) -> T:
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in template_dict.items() if k in field_names})
