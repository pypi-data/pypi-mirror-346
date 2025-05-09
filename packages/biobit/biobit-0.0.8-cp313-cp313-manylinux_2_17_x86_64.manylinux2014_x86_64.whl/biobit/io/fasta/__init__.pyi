from pathlib import Path
from types import TracebackType
from typing import Iterable, Self

from biobit.core.loc import IntoInterval
from biobit.io.protocols import ReadRecord, WriteRecord, IntoDecoding


class Record:
    id: str
    seq: str

    def __init__(self, id: str, seq: str): ...


class Reader(ReadRecord[Record]):
    def __init__(self, path: str | Path, compression: IntoDecoding | None = None): ...

    def read_record(self, into: Record | None = None) -> Record: ...

    def read_to_end(self) -> list[Record]: ...

    def __iter__(self) -> Reader: ...

    def __next__(self) -> Record: ...

    __hash__ = None  # type: ignore


class IndexedReader:
    def __init__(self, path: str | Path, compression: IntoDecoding | None = None): ...

    @property
    def path(self) -> Path: ...

    def fetch(self, seqid: str, interval: IntoInterval) -> str: ...

    def fetch_full_seq(self, seqid: str) -> str: ...

    __hash__ = None  # type: ignore


class Writer(WriteRecord[Record]):
    def __init__(self, path: Path, line_width: int | None = None): ...

    def write_record(self, record: Record) -> Self: ...

    def write_records(self, records: Iterable[Record]) -> Self: ...

    def flush(self) -> Self: ...

    def close(self) -> None: ...

    def __enter__(self) -> Writer: ...

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: TracebackType | None): ...
