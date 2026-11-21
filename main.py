#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261121.

Copies the pre-drawn image (entry.png, built by build_image.py) to the
grader's output directory. Standard library only, no network, and the
same bytes on every run.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
