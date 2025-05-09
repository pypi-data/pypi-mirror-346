from collections.abc import Sequence

from biobit.core.loc import Interval, IntoInterval, IntoOrientation
from biobit.io.bed import Bed12


class InvSegment:
    """
    Complementary sequence segments that are part of a larger inverted repeat.

    It's guaranteed that:
     * left segment doesn't overlap the right segment
     * left segment coordinates < right segment coordinates
    """

    def __init__(self, left: IntoInterval, right: IntoInterval): ...

    @property
    def left(self) -> Interval:
        """
        Left segment of the inverted repeat.
        """
        pass

    @property
    def right(self) -> Interval:
        """
        Right segment of the inverted repeat.
        """
        pass

    def brange(self) -> Interval:
        """
        A bounding range of the segment - minimum range that contains both the left and right arms of the segment.
        """
        pass

    def inner_gap(self) -> int:
        """
        The inner gap between the left and right segments of the inverted repeat.
        """
        pass

    def shift(self, shift: int):
        """
        Shift the entire segment by the given value(in place). Useful for map coordinates.
        """
        pass

    def __repr__(self) -> str: ...

    def __len__(self) -> int: ...

    def __eq__(self, other) -> bool: ...


class InvRepeat:
    """
    Inverted repeats composed of complementary segments separated by variable gaps.

    In terms of alignment scores, inverted repeat is locally optimal. That is, it can't be extended or shrunk to
    get a higher alignment score.
    """

    def __init__(self, segments: list[InvSegment]):
        """
        Construct a new inverted repeat from the given segments.
        Segments must not overlap and must be sorted by starting position (eg segment.brange().start).
        """
        pass

    @property
    def segments(self) -> Sequence[InvSegment]:
        """
        Segments of the inverted repeat.
        """
        pass

    def seqlen(self) -> int:
        """
        The total length of the sequence under the inverted repeat.
        """
        pass

    def inner_gap(self) -> int:
        """
        The inner gap between the left and right segments of the inverted repeat.
        """
        pass

    def right_brange(self) -> Interval:
        """
        A bounding range containing all right segments of the inverted repeat.
        """
        pass

    def left_brange(self) -> Interval:
        """
        A bounding range containing all left segments of the inverted repeat.
        """
        pass

    def brange(self) -> Interval:
        """
        A bounding range of the repeat - minimum range that contains all its segments.
        """
        pass

    def shift(self, offset: int) -> 'InvRepeat':
        """
        Shift the entire repeat by the given value(in place). Useful for map coordinates.
        """
        pass

    def seqranges(self) -> list[Interval]:
        """
        Ordered sequence blocks, i.e. sequence ranges, that underlay the inverted repeat.
        """
        pass

    def coverage(self) -> int:
        """
        The total number of base pairs covered by the inverted repeat.
        """
        pass

    def to_bed12(self, seqid: str, *args,
                 name: str = ".", score: int = 0, orientation: IntoOrientation = "=",
                 rgb: tuple[int, int, int] = (0, 0, 0)) -> Bed12:
        """
        Convert inverted repeat to a BED12 record. All arguments except the seqid should be passed as kwargs
        """
        pass
