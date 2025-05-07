"""cppcheck-suppressor module for cppcheck suppressions handling"""

import logging
from xml.etree.ElementTree import ElementTree
import xmlschema
from cppcheck_suppressor import schema_directory


logger = logging.getLogger(__name__)


def write_suppressions(suppressions: list, filename: str) -> int:
    """
    Writes given Cppcheck suppressions list to a file in XML format.

    The output file can be used as a parameter to run Cppcheck and to
    suppress the items in it.

    Args:
        suppressions: List of suppressions that are being written to
        the output file.
        filename: The output file name (and path) to where to write
        the suppressions.

    Return:
        Exit code representing if the suppression file was created
        successfully or not.
    """
    schema = xmlschema.XMLSchema(schema_directory)
    output = {}
    logger.debug(
        "Writing %d suppressions to output file %s...", len(suppressions), filename
    )
    if len(suppressions) > 0:
        output = {"suppress": suppressions}
    ss = schema.encode(output, path="/suppressions")
    ElementTree(ss).write(filename, xml_declaration=True, encoding="UTF-8")
    logger.debug("Suppressions written!")
    return 0
