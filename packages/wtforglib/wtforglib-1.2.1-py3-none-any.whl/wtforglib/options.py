"""Top-level module for Wtforg Library."""

import logging
import sys
from types import MappingProxyType
from typing import Dict, Optional, Union

OptionsDict = Dict[str, Union[str, int, bool]]

OPTIONS_DEBUG = "debug"
OPTIONS_TEST = "test"
OPTIONS_VERBOSE = "verbose"
LOG_LEVELS = MappingProxyType(
    {
        "crit": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    },
)


def log_level_name(level: int, default: str = "info") -> str:
    """Return logger level name.

    Parameters
    ----------
    level : int
        Level number
    default : str, optional
        Default if not matched, by default "info"

    Returns
    -------
    str
        Level name
    """
    for key, valor in LOG_LEVELS.items():
        if level == valor:
            return key
    return default


def basic_options(
    debug: Union[bool, int],
    test: bool,
    verbose: Union[bool, int],
) -> OptionsDict:
    """Return a dictionary of basic options.

    Parameters
    ----------
    debug : Union[bool, int]
        Sets debug: int in the returned dictionary
    test : bool
        Sets test: bool in the returned dictionary
    verbose : Union[bool, int]
        Sets verbose: int in the returned dictionary

    Returns
    -------
    OptionsDict
        Options dictionary
    """
    od: OptionsDict = {}
    od["debug"] = int(debug) if isinstance(debug, bool) else debug
    od["test"] = test
    od["verbose"] = int(verbose) if isinstance(verbose, bool) else verbose
    return od


class SimpleScribe:
    """Class for simple screen logging."""

    options: OptionsDict
    _errors: int

    def __init__(self, opts: Optional[OptionsDict] = None) -> None:
        """Construct a simple scribe object.

        Class to handle screen logging.

        Parameters
        ----------
        opts : OptionsDict Optional
            Options to merge with defaults
        """
        self._errors = 0
        self.options = {OPTIONS_DEBUG: 0, OPTIONS_VERBOSE: 0, OPTIONS_TEST: False}
        if opts is not None:
            self.options.update(opts)

    def debug(self, message: str) -> None:
        """Utility trace debug method."""
        if self.options[OPTIONS_DEBUG]:
            self._log_msg("DEBUG: {0}".format(message))

    def info(self, message: str) -> None:  # noqa: WPS110
        """Utility trace info method."""
        if self.options[OPTIONS_VERBOSE]:
            self._log_msg("INFO: {0}".format(message))

    def warning(self, message: str) -> None:
        """Utility trace warning method."""
        self._log_msg("WARNING: {0}".format(message))

    def warn(self, message: str) -> None:
        """Utility trace warn method."""
        self.warning(message)

    def error(self, message: str) -> None:
        """Utility trace error method."""
        self._log_msg("ERROR: {0}".format(message))
        self._errors += 1

    def _log_msg(self, message: str) -> None:
        """Write message to stderr."""
        print(message, file=sys.stderr)


class Options(SimpleScribe):
    """A class to handle Options."""

    options: OptionsDict

    def __init__(self, opts: Optional[OptionsDict] = None) -> None:
        """Options constructor.

        Class to manage options for the module.

        Parameters
        ----------
        opts : OptionsDict Optional
            Options to merge with defaults
        """
        super().__init__(opts)
        if int(self.options[OPTIONS_DEBUG]):
            self.debug(
                "created instance of class {0}".format(self.__class__.__name__),
                2,
            )

    def isdebug(self) -> bool:
        """Returns True if debug > 0."""
        return int(self.options[OPTIONS_DEBUG]) > 0

    def isverbose(self) -> bool:
        """Returns True if verbose > 0."""
        return int(self.options[OPTIONS_VERBOSE]) > 0

    def isnoop(self) -> bool:
        """Returns True if noop."""
        return bool(self.options.get("noop", False))

    def isforce(self) -> bool:
        """Returns True if noop."""
        return bool(self.options.get("force", False))

    def istest(self) -> bool:
        """Returns value of test flag."""
        return bool(self.options[OPTIONS_TEST])

    def debug(self, message: str, level: int = 1) -> None:
        """Utility debug method."""
        dl: int = int(self.options[OPTIONS_DEBUG])
        if self.options[OPTIONS_TEST] or dl >= level:
            super().debug(message)

    def verbose(self, message: str, level: int = 1) -> None:
        """Utility verbose method."""
        vl: int = int(self.options[OPTIONS_VERBOSE])
        if self.options[OPTIONS_TEST] or vl >= level:
            self.info(message)
