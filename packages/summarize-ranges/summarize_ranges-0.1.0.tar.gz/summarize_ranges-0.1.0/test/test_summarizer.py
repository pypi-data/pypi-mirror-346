import pytest
from summarize_ranges.ranges import RangeSummarizer


def testInitial() -> None:
    """
    If no text is given there must be no ranges.
    """
    s = RangeSummarizer()
    assert list(s.ranges()) == []


def testEmpty() -> None:
    """
    If no text is given and an empty string is added there must be no ranges.
    """
    s = RangeSummarizer()
    s.add("")
    assert list(s.ranges()) == []


def testNoDigitsInit() -> None:
    """
    If text with no digits is given in the constructor, there must be no ranges.
    """
    s = RangeSummarizer("hey")
    assert list(s.ranges()) == []


def testNoDigitsArg() -> None:
    """
    If text with no digits is given to add(), there must be no ranges.
    """
    s = RangeSummarizer()
    s.add("hey")
    assert list(s.ranges()) == []


def testOneNumberInit() -> None:
    """
    If text with one number is given to the constructor, there must be one range.
    """
    s = RangeSummarizer("88")
    assert list(s.ranges()) == [(88, 89)]


def testOneNumberArg() -> None:
    """
    If text with one number is given to add(), there must be one range.
    """
    s = RangeSummarizer()
    s.add("88")
    assert list(s.ranges()) == [(88, 89)]


def testNegativesRecognized() -> None:
    """
    Negative numbers are recognized by default.
    """
    s = RangeSummarizer()
    s.add("-88")
    assert list(s.ranges()) == [(-88, -87)]


def testNegativesRecognizedRequiringWordBoundaries() -> None:
    """
    Negative numbers can be recognized when word boundaries are required.
    """
    s = RangeSummarizer()
    s.add("abc -88")
    assert list(s.ranges()) == [(-88, -87)]


def testNegativesNotRecognizedAbsentWordBoundaries() -> None:
    """
    Negative numbers with no word boundaries are not recognized by default.
    """
    s = RangeSummarizer()
    s.add("a-88")
    assert list(s.ranges()) == [(88, 89)]


def testNegativesCanBeRecognizedNotRequiringWordBoundaries() -> None:
    """
    Negative numbers can be recognized if we don't require word boundaries.
    """
    s = RangeSummarizer(match_negatives=True, require_word_boundaries=False)
    s.add("abc-88def")
    assert list(s.ranges()) == [(-88, -87)]


@pytest.mark.parametrize("text", ("abc88", "88def", "abc88def"))
def testRequireWordBoundaries(text: str) -> None:
    """
    If word boundaries are required, numbers not properly bounded must be ignored.
    """
    s = RangeSummarizer(text)
    assert list(s.ranges()) == []


@pytest.mark.parametrize("text", ("abc88", "88def", "abc88def"))
def testDontRequireWordBoundaries(text: str) -> None:
    """
    If word boundaries are not required, numbers that are not words must be found.
    """
    s = RangeSummarizer(text, require_word_boundaries=False)
    assert list(s.ranges()) == [(88, 89)]


def testOneInterruptedRange() -> None:
    """
    A range interrupted by non-digit text must be recognized.
    """
    s = RangeSummarizer("abc 1 2 3 def 4 5 6 ghi")
    assert list(s.ranges()) == [(1, 7)]


def testTwoRanges() -> None:
    """
    Two ranges must be recognized.
    """
    s = RangeSummarizer("abc 1 2 3 def 5 6 7 ghi")
    assert list(s.ranges()) == [(1, 4), (5, 8)]


def testTwoRangesWithNegatives() -> None:
    """
    Two ranges with negative numbers must be recognized.
    """
    s = RangeSummarizer("abc -1 -2 -3 def -5 -6 -7 ghi")
    assert list(s.ranges()) == [(-7, -4), (-3, 0)]


def testThreeRanges() -> None:
    """
    Three ranges must be recognized.
    """
    s = RangeSummarizer("10 abc 1 2 3 def 5 6 7 ghi 11 12 xyz 9 13")
    assert list(s.ranges()) == [(1, 4), (5, 8), (9, 14)]


def testThreeRangesNoWordBoundaries() -> None:
    """
    Three ranges must be recognized when word boundaries are not required.
    """
    s = RangeSummarizer(
        "x10y abc _1_ 2 3 def 5 p6q 7 ghi 11 12 xyz 9 13", require_word_boundaries=False
    )
    assert list(s.ranges()) == [(1, 4), (5, 8), (9, 14)]
