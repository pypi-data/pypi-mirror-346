"""cppcheck-suppressor main function implementation module"""

import argparse
import logging
import sys
from cppcheck_suppressor.results import (
    cppcheck_errors_to_suppressions,
    get_cppcheck_errors,
)
from cppcheck_suppressor.suppressions import write_suppressions

logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    """
    Parses command line arguments for the main function.

    Returns:
        The parsed arguments in argparse.Namespace.
    """
    parser = argparse.ArgumentParser(
        prog="cppcheck-suppressor",
        description="A tool that creates suppressions for Cppcheck from its output.",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="cppcheck_errors.xml",
        help="Cppcheck output file in XML format. This includes the errors that are \
        added to the suppressions file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="baseline.xml",
        help="Output file name (and path) for the suppressions file.",
    )
    return parser.parse_args()


def main(inputfile: str, outputfile: str) -> int:
    """
    Creates a Cppcheck suppression file from results of
    Cppcheck errors. The suppression file is in xml format.

    The suppression file can be used as a baseline in any
    further Cppcheck analysis of the same project to observe
    new errors.

    Args:
        inputfile: The name (and path) of the Cppcheck results input
        file.
        outputfile: The name (and path) of the suppressions output
        file.

    Returns:
        Exit code representing if the suppression file was created
        successfully.
    """
    logging.basicConfig(level=logging.INFO)
    errors = get_cppcheck_errors(inputfile)
    suppressions = cppcheck_errors_to_suppressions(errors)
    return write_suppressions(suppressions, outputfile)


def cli() -> int:
    """
    Creates a Cppcheck suppression file from results of
    Cppcheck errors. The suppression file is in xml format.

    The suppression file can be used as a baseline in any
    further Cppcheck analysis of the same project to observe
    new errors.

    This function is meant to be used from command line as a
    script, and it will parse the command line arguments.
    """
    args = _parse_args()
    return main(args.file, args.output)


if __name__ == "__main__":
    sys.exit(cli())
