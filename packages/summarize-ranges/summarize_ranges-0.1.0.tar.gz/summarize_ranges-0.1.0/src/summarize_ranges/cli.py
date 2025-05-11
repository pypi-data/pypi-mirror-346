import sys
import argparse

from summarize_ranges import ranges
from summarize_ranges.ranges import RangeSummarizer


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Collect numbers found on standard input and print a summary of the "
            "consecutive ranges found."
        ),
    )

    parser.add_argument(
        "--ignore-word-boundaries",
        "--iwb",
        action="store_false",
        dest="require_word_boundaries",
        help=(
            "Do not require numbers to be separated by word boundaries. For example, "
            "wih this setting the number 33 would be extracted from input text "
            "containing 'abc33def'."
        ),
    )

    parser.add_argument(
        "--ignore-negatives",
        "--in",
        action="store_false",
        dest="match_negatives",
        help=(
            "Do not look for negative numbers. Under this option, the string -33 in "
            "the input would result in the number 33 being collected."
        ),
    )

    parser.add_argument(
        "--python",
        action="store_true",
        help="Print Python closed-open ranges (i.e., the upper bound is not included).",
    )

    parser.add_argument(
        "--tsv",
        action="store_true",
        help=(
            "Ranges are printed one per line with high and low values separated by a "
            "TAB. If not given, print ranges in a human-friendly manner."
        ),
    )

    args = parser.parse_args()
    high_adjust = 0 if args.python else 1

    rs = RangeSummarizer(
        match_negatives=args.match_negatives,
        require_word_boundaries=args.require_word_boundaries,
    )

    for line in sys.stdin:
        rs.add(line)

    if args.tsv:
        for low, high in rs.ranges():
            high -= high_adjust
            print(f"{low}\t{high}")
    else:
        for count, (low, high) in enumerate(rs.ranges(), start=1):
            high -= high_adjust
            if low == high:
                print(f"Range {count}: {low}")
            else:
                print(f"Range {count}: {low} to {high}")
