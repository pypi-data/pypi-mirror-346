# Local
from scope.callgraph.utils import stable_hash


class Range(object):
    def __init__(self, start_line, start_column, end_line, end_column):
        """Initialize a Range object representing a text span in a file.

        Args:
            start_line (int): The starting line number (1-indexed)
            start_column (int): The starting column number (1-indexed)
            end_line (int): The ending line number (1-indexed)
            end_column (int): The ending column number (1-indexed)
        """
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column

    def __eq__(self, other):
        """Check if this Range is equal to another Range.

        Args:
            other (Range): Another Range object to compare with

        Returns:
            bool: True if both ranges have identical start and end positions, False otherwise
        """
        if not isinstance(other, Range):
            return NotImplemented

        start_line_eq = self.start_line == other.start_line
        start_col_eq = self.start_column == other.start_column
        end_line_eq = self.end_line == other.end_line
        end_col_eq = self.end_column == other.end_column
        return all([start_line_eq, start_col_eq, end_line_eq, end_col_eq])

    def contains(self, other) -> bool:
        """Check if this Range completely contains another Range.

        Args:
            other (Range): Another Range object to check containment for

        Returns:
            bool: True if this range completely contains the other range, False otherwise
        """
        if not isinstance(other, Range):
            return NotImplemented
        return (
            self.start_line <= other.start_line
            and self.end_line >= other.end_line
            and (
                self.start_line < other.start_line
                or (
                    self.start_line == other.start_line
                    and self.start_column <= other.start_column
                )
            )
            and (
                self.end_line > other.end_line
                or (
                    self.end_line == other.end_line
                    and self.end_column >= other.end_column
                )
            )
        )

    def __hash__(self):
        """Generate a hash value for this Range object.

        Returns:
            int: A stable hash value based on the range's coordinates
        """
        return stable_hash(
            {
                "start_line": self.start_line,
                "start_column": self.start_column,
                "end_line": self.end_line,
                "end_column": self.end_column,
            },
            as_int=True,
        )

    def __str__(self):
        """Get a string representation of this Range.

        Returns:
            str: A string in the format "Range([start_line:start_column] - [end_line:end_column])"
        """
        return f"Range([{self.start_line}:{self.start_column}] - [{self.end_line}:{self.end_column}])"

    def to_dict(self):
        """Convert the Range to a dictionary representation.

        Returns:
            dict: A dictionary containing the range's coordinates
        """
        return {
            "start_line": self.start_line,
            "start_column": self.start_column,
            "end_line": self.end_line,
            "end_column": self.end_column,
        }

    def to_list(self):
        """Convert the Range to a list representation.

        Returns:
            list: A list containing [start_line, start_column, end_line, end_column]
        """
        return [self.start_line, self.start_column, self.end_line, self.end_column]

    def invalid(self):
        """Check if this Range is invalid (has any coordinate set to -1).

        Returns:
            bool: True if any coordinate is -1, False otherwise
        """
        start_line_invalid = self.start_line == -1
        start_col_invalid = self.start_column == -1
        end_line_invalid = self.end_line == -1
        end_col_invalid = self.end_column == -1
        return any(
            [
                start_line_invalid,
                start_col_invalid,
                end_line_invalid,
                end_col_invalid,
            ]
        )

    def height(self):
        """Calculate the height of this Range in lines.

        Returns:
            int: The number of lines spanned by this range (end_line - start_line)
        """
        return self.end_line - self.start_line

    def width(self):
        """Calculate the width of this Range in columns.

        Returns:
            int: The maximum column number in this range
        """
        return max(self.end_column, self.start_column)
