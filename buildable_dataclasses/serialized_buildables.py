import logging
from abc import ABC
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic, NewType, TypeVar, cast

from misc_python_utils.beartypes import NeList
from nested_dataclass_serialization.dataclass_hashing import hash_dataclass
from nested_dataclass_serialization.dataclass_serialization import (
    deserialize_dataclass,
    serialize_dataclass,
)

from buildable_dataclasses.buildable import Buildable

SerializedBuildable = NewType("SerializedBuildable", str)

logger = logging.getLogger(__name__)

BuildableT = TypeVar("BuildableT", bound=Buildable)


@dataclass
class UniqueSerializedBuildables(
    Iterable[SerializedBuildable],
    Buildable,
    Generic[BuildableT],
):
    buildables: NeList[BuildableT]
    serialized_exam_scorings: NeList[SerializedBuildable] = field(init=False)

    def _build_self(self) -> None:
        hashed = [hash_dataclass(e) for e in self.buildables]
        self.serialized_exam_scorings = [
            SerializedBuildable(serialize_dataclass(e)) for e in self.buildables
        ]
        assert len(set(hashed)) == len(
            hashed,
        ), f"{len(set(hashed))=}!={len(hashed)=}"

    def __iter__(self) -> Iterator[SerializedBuildable]:
        yield from self.serialized_exam_scorings


@dataclass
class SequentialMainProcessBuilder(ABC, Buildable, Iterable[BuildableT]):
    """
    builds things sequentially in same main-process
    """

    serialized_buildables: UniqueSerializedBuildables[BuildableT] = field(repr=True)
    built_buildables: NeList[BuildableT] = field(init=False, repr=True)

    def _build_self(self) -> None:
        self.built_buildables = [
            cast(BuildableT, deserialize_dataclass(s)).build()
            for s in self.serialized_buildables.serialized_exam_scorings
        ]

    def __iter__(self) -> Iterator[BuildableT]:
        yield from self.built_buildables
