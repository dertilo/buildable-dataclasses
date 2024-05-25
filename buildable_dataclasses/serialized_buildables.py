import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import NewType

from misc_python_utils.beartypes import NeList
from nested_dataclass_serialization.dataclass_hashing import hash_dataclass
from nested_dataclass_serialization.dataclass_serialization import serialize_dataclass

from buildable_dataclasses.buildable import Buildable

SerializedBuildable = NewType("SerializedBuildable", str)

logger = logging.getLogger(__name__)


@dataclass
class SerializedBuildables(Iterable[SerializedBuildable], Buildable):
    buildables: NeList[Buildable]
    serialized_exam_scorings: NeList[SerializedBuildable] = field(init=False)

    def _build_self(self) -> None:
        hashed_experiments = [hash_dataclass(e) for e in self.buildables]
        self.serialized_exam_scorings = [
            SerializedBuildable(serialize_dataclass(e)) for e in self.buildables
        ]
        assert len(set(hashed_experiments)) == len(
            hashed_experiments,
        ), f"{len(set(hashed_experiments))=}!={len(hashed_experiments)=}"

    def __iter__(self) -> Iterator[SerializedBuildable]:
        yield from self.serialized_exam_scorings
