# HiCPlot/Cli.py
# ----------------------------------------------------------------------
# Hi‑C Plotting command‑line wrapper
#
# This tiny front‑end lets you run any of the plotting scripts shipped
# with HiCPlot via one unified executable:
#
#     $ HiCPlot <tool> [tool‑specific options...]
#
# Typing either `HiCPlot -h` for global help or
# `HiCPlot <tool> -h` for a tool’s own help works naturally.
# ----------------------------------------------------------------------

from __future__ import annotations

import argparse
import sys
from typing import Callable, Dict, List, Optional

# ----------------------------------------------------------------------
# Import individual plotting entry points
# ----------------------------------------------------------------------
# Ensure these imports match your actual file structure and tool names
# Example: from HiCPlot.SquHeatmap import main as _run_squ
# For the purpose of this example, I'll use placeholders if the exact
# HiCPlot internal scripts aren't fully known beyond TriHeatmap.
# You'll need to ensure these paths are correct for your HiCPlot installation.

# Assuming these are the correct import paths for your HiCPlot tools:
from HiCPlot.SquHeatmap import main as _run_squ
from HiCPlot.SquHeatmapTrans import main as _run_squTrans
from HiCPlot.TriHeatmap import main as _run_tri # This one is key for your current use
from HiCPlot.DiffSquHeatmap import main as _run_diff
from HiCPlot.DiffSquHeatmapTrans import main as _run_diffTrans
from HiCPlot.upper_lower_triangle_heatmap import main as _run_ul
from HiCPlot.NGStrack import main as _run_track

# ----------------------------------------------------------------------
# Mapping of sub‑command → function
# ----------------------------------------------------------------------
_SUBCOMMANDS: Dict[str, Callable[[Optional[List[str]] | None], None]] = {
    "SquHeatmap": _run_squ,
    "SquHeatmapTrans": _run_squTrans,
    "TriHeatmap": _run_tri,
    "DiffSquHeatmap": _run_diff,
    "DiffSquHeatmapTrans": _run_diffTrans,
    "upper_lower_triangle_heatmap": _run_ul,
    "NGStrack": _run_track,
}

# One‑line descriptions shown in the top‑level help
_SUBCOMMAND_DESCR: Dict[str, str] = {
    "SquHeatmap": "Square intra‑chromosomal heatmap",
    "SquHeatmapTrans": "Square inter‑chromosomal heatmap",
    "TriHeatmap": "Triangular intra‑chromosomal heatmap", # Used in your command
    "DiffSquHeatmap": "Differential square heatmap",
    "DiffSquHeatmapTrans": "Differential square inter‑heatmap",
    "upper_lower_triangle_heatmap": "Split‑triangle heatmap (upper vs lower)",
    "NGStrack": "Plot multiple NGS tracks",
}

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    """Return the top‑level parser with a sub‑parser per plotting tool."""
    parser = argparse.ArgumentParser(
        prog="HiCPlot",
        description="Hi‑C plotting utility (wrapper for individual tools)",
    )

    subparsers = parser.add_subparsers(
        title="Available tools",
        dest="cmd", # This is crucial: it stores the name of the chosen subcommand
        metavar="<tool>",
        required=True,  # Python ≥3.7, ensures a tool must be specified
    )

    # Each sub‑parser owns its own -h/--help so that
    # `HiCPlot <tool> -h` prints the real tool’s usage text.
    for name, func in _SUBCOMMANDS.items():
        help_line = _SUBCOMMAND_DESCR.get(name, "(no description)")
        sp = subparsers.add_parser(
            name,
            help=help_line,        # shows up in `HiCPlot -h`
            description=help_line, # shows up in `HiCPlot <tool> -h`
            add_help=False,        # let the tool itself define -h/--help
        )
        sp.set_defaults(_entry=func) # Associate the submand with its function

    return parser


# ----------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------
def main(argv: Optional[List[str]] | None = None) -> None:
    """
    Dispatch to the selected plotting tool, forwarding every remaining
    CLI token untouched.
    """
    # --- Start of Debugging Print Statements ---
    print(f"DEBUG [Cli.py main]: Initial sys.argv received by script: {sys.argv}", file=sys.stderr)
    passed_argv_to_func = argv # Store the argument if 'main' was called directly with an argv list
    # --- End of Debugging Print Statements ---

    argv = sys.argv[1:] if argv is None else argv

    # --- Start of Debugging Print Statements ---
    print(f"DEBUG [Cli.py main]: Argument list 'argv' before parsing (should be sys.argv[1:] or passed_argv_to_func): {argv}", file=sys.stderr)
    if passed_argv_to_func is not None:
        print(f"DEBUG [Cli.py main]: 'main' was called with argv: {passed_argv_to_func}", file=sys.stderr)
    # --- End of Debugging Print Statements ---

    parser = _build_parser()

    try:
        # We purposely use *known* (not *intermixed*) parsing.  That avoids the
        # Python‑3.12 restriction that forbids `parse_*intermixed*` when any
        # descendant parser defines a `nargs=argparse.REMAINDER` positional.
        ns, rest = parser.parse_known_args(argv)

        # --- Start of Debugging Print Statements ---
        print(f"DEBUG [Cli.py main]: After parse_known_args:", file=sys.stderr)
        print(f"DEBUG [Cli.py main]:   Parsed namespace (ns): {ns}", file=sys.stderr)
        print(f"DEBUG [Cli.py main]:   Remaining arguments (rest): {rest}", file=sys.stderr)
        # --- End of Debugging Print Statements ---

    except argparse.ArgumentError as e:
        print(f"ERROR [Cli.py main]: ArgumentError during initial parsing: {e}", file=sys.stderr)
        parser.print_help(sys.stderr) # Print help for the main HiCPlot command
        sys.exit(2) # Exit with an error code
    except SystemExit as e: # Handles errors from parser like unrecognized arguments
        print(f"ERROR [Cli.py main]: SystemExit during initial parsing (likely argparse error): {e}", file=sys.stderr)
        # Argparse might have already printed a message.
        # If exit code is 0 (e.g. from -h for main parser), let it pass.
        if e.code != 0:
             # parser.print_usage(sys.stderr) # Argparse usually does this.
             sys.exit(e.code or 1) # Propagate exit code or use 1
        else:
            sys.exit(0)


    # Ensure a command was actually parsed and an entry point exists
    if not hasattr(ns, '_entry') or ns.cmd is None:
        print(f"ERROR [Cli.py main]: No tool command was recognized or namespace is incomplete. ns: {ns}", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    # The selected tool’s main()
    entry: Callable[[Optional[List[str]] | None], None] = getattr(ns, "_entry")

    # If the very next token is -h/--help, run the tool’s help directly.
    # This is a special handling for 'HiCPlot <tool> -h'
    if rest and rest[0] in ("-h", "--help"):
        print(f"DEBUG [Cli.py main]: Detected '-h' or '--help' for tool '{ns.cmd}'. Calling tool's help.", file=sys.stderr)
        entry(["-h"]) # Pass only '-h' to the tool's main function
    else:
        print(f"DEBUG [Cli.py main]: Dispatching to tool '{ns.cmd}' with arguments: {rest or 'None'}", file=sys.stderr)
        entry(rest or None) # Pass the remaining arguments to the tool's main function


if __name__ == "__main__":
    # When run as a script, sys.argv is automatically used by main() if argv is None.
    main()