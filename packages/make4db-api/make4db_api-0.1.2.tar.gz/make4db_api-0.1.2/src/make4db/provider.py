"provider object API"

from argparse import ArgumentParser
from enum import StrEnum
from typing import Any, Callable, Iterable, NamedTuple, Protocol, Self, TextIO, TypeAlias

DDL: TypeAlias = str | Iterable[str]
PySqlFn: TypeAlias = Callable[[Any, str, bool], DDL] | Callable[[str, bool], DDL]


class SchObj(NamedTuple):
    sch: str
    obj: str

    def __str__(self) -> str:
        return f"{self.sch}.{self.obj}"

    @classmethod
    def make(cls: type[Self], sch: str, obj: str) -> Self:
        return cls(sch.lower(), obj.lower())


class Feature(StrEnum):
    AutoRefresh = "auto_refresh"
    CreateOrReplace = "create_or_replace"
    DropDatabaseOrphans = "drop_db_orphans"


class DbAccess(Protocol):
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Any, **kwargs: Any) -> bool | None: ...
    def execsql(self, sql: str, output: TextIO) -> None: ...
    def iterdep(self, objs: Iterable[SchObj]) -> Iterable[tuple[SchObj, SchObj]]: ...
    def py2sql(self, fn: Callable[[Any, str, bool], DDL], object: str, replace: bool) -> Iterable[str]: ...
    def drop_except(self, objs: set[SchObj]) -> Iterable[str]: ...


class DbProvider(Protocol):
    def dbacc(self, conn_args: dict[str, Any]) -> DbAccess: ...
    def version(self) -> str: ...
    def name(self) -> str: ...
    def add_db_args(self, parser: ArgumentParser): ...
    def supports_feature(self, feature: Feature) -> bool: ...
