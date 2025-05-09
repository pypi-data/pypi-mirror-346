"""Top-level module for wtforglib Library."""

import platform
import re
import subprocess  # noqa: S404
from pathlib import Path
from typing import ClassVar, Optional

from wtforglib.errors import ShellError
from wtforglib.kinds import FileName

WINDOZE = "Windows"

if platform.system() == WINDOZE:
    from socket import getfqdn  # noqa: WPS433

WINDOZE_NOT_IMPLEMENTED = "{0} is not implemented on Windows"


class WtfSingleton:
    """Singleton class."""

    dn: ClassVar[str] = ""
    hn: ClassVar[str] = ""

    def __new__(cls):  # pragma no cover
        """Creates new singleton if one does not exist."""
        if not hasattr(cls, "instance"):  # noqa: WPS421
            cls.instance = super(WtfSingleton, cls).__new__(cls)  # noqa: WPS608
        return cls.instance


def domainname(test: bool = False) -> str:  # noqa: WPS605, WPS231
    """Return hosts domain name.

    Parameters
    ----------
    test : bool Optional
        Default False, when true return example.com

    Returns
    -------
    str
        domain name

    Raises
    ------
    ShellError
        if subprocess return code is not 0
    """
    if not WtfSingleton.dn:
        if test:
            WtfSingleton.dn = "example.com"
        elif platform.system() == WINDOZE:
            parts = getfqdn().split(".", 1)
            if len(parts) == 2:
                WtfSingleton.dn = parts[1]
            else:
                WtfSingleton.dn = "unknown"
        else:
            sp_result = subprocess.run(
                ["hostname", "-d"],
                capture_output=True,
                encoding="utf8",
            )
            if sp_result.returncode != 0:  # pragma no cover
                raise ShellError("Failed to determine host's domain name")
            WtfSingleton.dn = sp_result.stdout.rstrip()
    return WtfSingleton.dn


def hostname(test: bool = False) -> str:  # noqa: WPS605, WPS231
    """Return hosts' hostname.

    Parameters
    ----------
    test : bool Optional
        Default False, when true return nombre

    Returns
    -------
    str
        hostname

    Raises
    ------
    ShellError
        if subprocess return code is not 0
    """
    if not WtfSingleton.hn:
        if test:
            WtfSingleton.hn = "nombre"
        elif platform.system() == WINDOZE:
            parts = getfqdn().split(".", 1)
            if parts:
                WtfSingleton.hn = parts[0]
            else:
                WtfSingleton.hn = "unknown"
        else:
            sp_result = subprocess.run(
                ["hostname"],
                capture_output=True,
                encoding="utf8",
            )
            if sp_result.returncode != 0:  # pragma no cover
                raise ShellError("Failed to determine hostname")
            WtfSingleton.hn = sp_result.stdout.rstrip()
    return WtfSingleton.hn


def strtobool(rts: str) -> bool:
    """Covert string rts to boolean."""
    return rts.lower() in {"true", "1", "t", "y", "yes"}


def windoze_not_implemented(foo_name: str) -> None:
    """Raised and exception if platform is Windows.

    Parameters
    ----------
    foo_name : str
        Name of function not supported

    Raises
    ------
    NotImplementedError
        When platform is Windows
    """
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(foo_name),
        )  # pragma: no cover


def unix_basename(fn: FileName, ext: Optional[str] = None) -> str:
    """Return unix basename of file name.

    Parameters
    ----------
    fn : FileName
        The file to get basename of
    ext : str Optional
        File extension

    Returns
    -------
    str
        unix basename of file name
    """
    rtn = Path(fn).name
    if ext:
        return re.sub("{0}$".format(ext), "", rtn)
    return rtn
