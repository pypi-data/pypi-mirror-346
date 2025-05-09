from typing import Any

from biobit.core.loc import Interval, Orientation


class Peak:
    @property
    def interval(self) -> Interval: ...

    @property
    def value(self) -> float: ...

    @property
    def summit(self) -> int: ...


class HarvestRegion:
    @property
    def contig(self) -> str: ...

    @property
    def orientation(self) -> Orientation: ...

    @property
    def interval(self) -> Interval: ...

    @property
    def signal(self) -> list[Interval]: ...

    @property
    def control(self) -> list[Interval]: ...

    @property
    def modeled(self) -> list[Interval]: ...

    @property
    def raw_peaks(self) -> list[Peak]: ...

    @property
    def filtered_peaks(self) -> list[Peak]: ...


class Harvest:
    @property
    def comparison(self) -> Any: ...

    @property
    def regions(self) -> list[HarvestRegion]: ...
