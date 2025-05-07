from __future__ import annotations
import argparse
import sys
from typing import Callable, Dict, List, Optional
from HiCPlot.SquHeatmap import main as _run_squ
from HiCPlot.SquHeatmapTrans import main as _run_squTrans
from HiCPlot.TriHeatmap import main as _run_tri
from HiCPlot.DiffSquHeatmap import main as _run_diff
from HiCPlot.DiffSquHeatmapTrans import main as _run_diffTrans
from HiCPlot.upper_lower_triangle_heatmap import main as _run_ul
from HiCPlot.NGStrack import main as _run_track

"""
HiCPlot command-line wrapper.

`HiCPlot -h` now shows every plotting tool with a succinct description.
Each description is defined once in _SUBCOMMAND_DESCR below.
"""

_SUBCOMMANDS: Dict[str, Callable[[Optional[List[str]]], None]] = {
    "SquHeatmap": _run_squ,
    "SquHeatmapTrans": _run_squTrans,
    "TriHeatmap": _run_tri,
    "DiffSquHeatmap": _run_diff,
    "DiffSquHeatmapTrans": _run_diffTrans,
    "upper_lower_triangle_heatmap": _run_ul,
    "NGStrack": _run_track,
}

# ----------------------------------------------------------------------
# One-line descriptions that appear in the top-level help
# ----------------------------------------------------------------------
_SUBCOMMAND_DESCR: Dict[str, str] = {
    "SquHeatmap": "Square intra-chromosomal heatmap",
    "SquHeatmapTrans": "Square inter-chromosomal heatmap",
    "TriHeatmap": "Triangular intra-chromosomal heatmap",
    "DiffSquHeatmap": "Differential square heatmap",
    "DiffSquHeatmapTrans": "Differential square inter-heatmap",
    "upper_lower_triangle_heatmap": "Split-triangle heatmap (upper vs lower)",
    "NGStrack": "Plot multiple NGS tracks",
    }

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    """Return the top-level parser with a sub-parser per tool."""
    parser = argparse.ArgumentParser(
        prog="HiCPlot",
        description="Hi-C plotting utility (wrapper for individual tools)",
    )

    subparsers = parser.add_subparsers(
        title="Available tools",
        dest="cmd",
        metavar="<tool>",
        required=True,  # Python >=3.7
    )

    for name, func in _SUBCOMMANDS.items():
        help_line = _SUBCOMMAND_DESCR.get(name, "(no description)")
        sp = subparsers.add_parser(
            name,
            help=help_line,          # appears in `HiCPlot -h`
            description=help_line,   # appears in `HiCPlot <tool> -h`
            add_help=False,          # let the tool own its -h/--help
        )
        sp.set_defaults(_entry=func)
        # Pass through *any* remaining CLI args to the sub-tool unchanged.
        sp.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    return parser


# ----------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------
def main(argv: Optional[List[str]] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    parser = _build_parser()

    # Accept inter-mixed options so both
    #   $ HiCPlot -h
    #   $ HiCPlot SquHeatmap -h
    # work naturally.
    ns, rest = parser.parse_known_intermixed_args(argv)
    entry: Callable[[Optional[List[str]]], None] = getattr(ns, "_entry")

    # If the *next* token is -h/--help, run the tool's help directly.
    if rest and rest[0] in ("-h", "--help"):
        entry(["-h"])
        return

    # Otherwise run the selected tool with whatever args remain.
    entry(rest)


if __name__ == "__main__":
    main()
