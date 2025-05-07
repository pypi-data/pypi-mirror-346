"""Top-level module for Wtforg Library."""

import errno
import os
from pathlib import Path
from typing import NoReturn

from wtforglib.kinds import Fspec


class ShellError(Exception):
    """Raised when subprocess resultcode not 0."""


def raise_filenotfound(filenm: Fspec) -> NoReturn:
    """Raises a FileNotFoundError execption for the given filenm.

    Parameters
    ----------
    filenm : Union[str,PathLike[str]]
        The yaml file to load

    Raises
    ------
    FileNotFoundError
        FileNotFoundError
    """
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(filenm))


def raise_filenotfound_if(filenm: Fspec) -> None:
    """Call raise_filenotfound for the given filenm if it doesn't exist.

    Parameters
    ----------
    filenm : Fspec
        Name of the file to test
    """
    fp = Path(filenm)
    if not fp.exists():
        raise_filenotfound(filenm)
    if not fp.is_file():
        raise_filenotfound(filenm)
