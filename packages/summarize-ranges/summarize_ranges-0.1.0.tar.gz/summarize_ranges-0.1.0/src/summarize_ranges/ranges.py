from re import compile
from itertools import count
from typing import Iterator, Tuple


class RangeSummarizer:
    """
    Examine text for integers and provide a method to summarize the contiguous ranges.
    """

    def __init__(
        self,
        initial_text=None,
        match_negatives: bool = True,
        require_word_boundaries: bool = True,
    ) -> None:
        self.numbers: set[int] = set()
        if require_word_boundaries:
            left = r"(?<!\w)"
            right = r"(?!\w)"
        else:
            left = right = ""
        negatives = "-?" if match_negatives else ""
        self.regex = compile(rf"{left}({negatives}\d+){right}")

        if initial_text:
            self.add(initial_text)

    def add(self, text: str) -> None:
        """
        Extract numbers from the text and add them to self.
        """
        for match in self.regex.finditer(text):
            number = int(match.group(0))
            self.numbers.add(number)

    def ranges(self) -> Iterator[Tuple[int, int]]:
        """
        """
        numbers = set(self.numbers)
        while numbers:
            low = min(numbers)
            for number in count(low):
                if number in numbers:
                    numbers.remove(number)
                else:
                    yield (low, number)
                    break
