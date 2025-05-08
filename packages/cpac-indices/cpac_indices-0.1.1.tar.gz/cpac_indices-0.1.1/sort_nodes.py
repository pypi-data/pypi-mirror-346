#!/usr/bin/env python3
# Copyright (C) 2025  C-PAC Developers

# This file is part of C-PAC.

# C-PAC is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# C-PAC is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with C-PAC. If not, see <https://www.gnu.org/licenses/>.
"""Sort nodes in a directory."""

import argparse
import os
from pathlib import Path
import re
from typing import cast, Optional, TypeAlias

_PATTERN = r"(_\d+)(?=(?:_\d+)*$)"
IndexType: TypeAlias = Optional[int | tuple[int, int]]


def _coerce_to_path(path: Path | str) -> Path:
    """Coerce a string or Path to a Path."""
    if isinstance(path, str):
        path = Path(path)
    return path


def _drop_underscore(index: str) -> int:
    """Drop leading underscore and convert to an integer."""
    return int(index.lstrip("_"))


def grab_index(path: Path | str) -> tuple["Index", Path]:
    """Grab the index from a filepath."""
    path = _coerce_to_path(path)
    index: IndexType = None
    filename = path.stem
    matches = re.findall(_PATTERN, filename)
    if matches:
        if len(matches) == 2:  # noqa: PLR2004
            index = cast(IndexType, tuple(_drop_underscore(match) for match in matches))
        if len(matches) == 1:
            index = _drop_underscore(matches[0])
    return Index(index), path


class Index:
    """A C-PAC node index."""

    def __init__(self, index: Optional[int | tuple[int, int]]):
        """Initialize an Index instance."""
        self.index = index

    def __repr__(self) -> str:
        """Return a string representation of the Index instance."""
        return f"Index({self.index})"

    def __str__(self) -> str:
        """Return a string representation of the Index instance."""
        if isinstance(self.index, tuple):
            return ".".join(f"{i}" for i in self.index)
        return f"{self.index}"

    def __eq__(self, other: object) -> bool:
        """Compare two Index instances for equality."""
        if not isinstance(other, Index):
            return False
        return self.index == other.index

    def __gt__(self, other: "Index") -> bool:
        """Compare two Index instances for greater than."""
        if other.index is None:
            return False
        if self.index is None:
            return True
        if isinstance(self.index, tuple) and isinstance(other.index, tuple):
            return self.index > other.index
        if isinstance(self.index, tuple) and isinstance(other.index, int):
            return self.index[0] >= other.index
        if isinstance(self.index, int) and isinstance(other.index, tuple):
            return self.index > other.index[0]
        assert isinstance(self.index, int) and isinstance(other.index, int)
        return self.index > other.index

    def __lt__(self, other: "Index") -> bool:
        """Compare two Index instances for less than."""
        if other.index is None:
            return True
        if self.index is None:
            return False
        if isinstance(self.index, tuple) and isinstance(other.index, tuple):
            return self.index < other.index
        if isinstance(self.index, tuple) and isinstance(other.index, int):
            return self.index[0] < other.index
        if isinstance(self.index, int) and isinstance(other.index, tuple):
            return self.index <= other.index[0]
        assert isinstance(self.index, int) and isinstance(other.index, int)
        return self.index < other.index


def gather_subdirectories(wd: Path | str) -> list[str]:
    """Gather and sort subdirectories in the given working directory."""
    paths = {
        (Path(root) / _d).stem
        for root, dirs, _ in os.walk(wd)
        for _d in dirs
        if re.search(_PATTERN, _d)
    }
    return sorted(paths, key=grab_index)


def main() -> None:
    """Sort nodes from commandline."""
    parser = argparse.ArgumentParser(description="Sort nodes in a directory.")
    parser.add_argument("directory", type=str, help="Directory to sort nodes in.")
    parser.add_argument(
        "--output",
        type=str,
        help="Output file to write sorted nodes to.",
        required=False,
    )
    args = parser.parse_args()

    sorted_paths = gather_subdirectories(args.directory)
    file = Path(args.output).open("w") if args.output else None
    for path in sorted_paths:
        print(path, file=file)
    if file:
        file.close()
        print(f"Sorted nodes written to: {args.output}")  # noqa: T201


if __name__ == "__main__":
    main()
