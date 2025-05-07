"""cppcheck-suppressor module ofr cppcheck results handling"""

import logging
import xmlschema
from cppcheck_suppressor import schema_directory

logger: logging.Logger = logging.getLogger(__name__)


def get_cppcheck_errors(filename: str) -> list:
    """
    Parses Cppcheck results file and returns the errors included in the file.

    Args:
        filename: The Cppcheck results (input) file. This should be in xml
        format.

    Returns:
        The errors from the Cppcheck results file (the content of the errors
        element).
    """
    schema = xmlschema.XMLSchema(schema_directory)
    logger.debug("Reading Cppcheck errors from .%s...", filename)
    errors = schema.decode(filename, "/results/errors", validation="strict")
    if errors is None:
        errors = {"error": []}
    logger.debug("Found %d errors from the file!", len(errors["error"]))
    return errors["error"]


def cppcheck_errors_to_suppressions(errors: list) -> list:
    """
    Creates a list of suppressions out of the errors from Cppcheck results.

    In case the error has more than one location in the results, this
    function cretes suppressions only for the first location.

    Args:
        errors: The list of errors that need to be suppressed. Use
        get_cppcheck_errors to read them from a file, for example.

    Return:
        A list of suppressions that suppresses the given errors.
    """
    suppressions = []
    logger.debug("Translating %d errors to suppressions...", len(errors))
    for error in errors:
        logger.debug("Tranlating error %s", error)
        error_location = next(iter(error["location"]), None)
        if error_location is not None:
            suppressions.append(
                {
                    "id": error["@id"],
                    "fileName": error_location["@file"],
                    "lineNumber": error_location["@line"],
                }
            )
    logger.debug("Translated errors to %d suppressions!", len(suppressions))
    return suppressions
