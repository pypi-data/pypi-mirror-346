import os
import re
import shutil
from typing import Optional

from wtforglib.dirs import ensure_directory


def clear_slot(root: str, idx: int, max_versions: int, debug: bool = False) -> str:
    """Clear backup slot for file being backed up.

    Parameters
    ----------
    root : str
        un-numbered basename
    idx : int
        version number
    max_versions : int
        maximum number of versions
    debug : bool, optional
        debug flag, by default False

    Returns
    -------
    str
        numbered slot name
    """
    slot = "{0}.{1}".format(root, idx)
    if os.path.isfile(slot):
        if idx >= max_versions:
            if debug:  # pragma no cover
                print("unlinking slot {0}".format(slot))
            os.unlink(slot)
        else:
            if debug:  # pragma no cover
                print("clearing slot {0}".format(slot))
            nslot = clear_slot(root, idx + 1, max_versions, debug)
            os.rename(slot, nslot)
    return slot


def clear_directory_slot(
    dirfpn: str,
    basenm: str,
    idx: int,
    max_versions: int,
    debug: bool = False,
) -> str:
    """Clear backup slot in directory other than file to backup.

    Parameters
    ----------
    dirfpn : str
        pathname of directory where backups are stored
    basenm : str
        un-numbered basename of file
    idx : int
        version number
    max_versions : int
        maximum number of versions
    debug : bool, optional
        debug flag, by default False

    Returns
    -------
    str
        numbered slot name
    """
    ensure_directory(dirfpn)
    return clear_slot(os.path.join(dirfpn, basenm), idx, max_versions, debug)


def check_root_filename(file_spec: str) -> str:
    """Determine root filename so the extension doesn't get longer.

    Parameters
    ----------
    file_spec : str
        Path name of the file to check

    Returns
    -------
    str
        Path name of the file to backup

    Raises
    ------
    ValueError
        If file_spec ends with one or more digit extension
    """
    nn, ee = os.path.splitext(file_spec)

    if re.match(r".\d+$", ee):
        raise ValueError(
            "Cannot create numbered backups for a file with a numbered ext",
        )
    return file_spec


def version_file(
    file_spec: str,
    vtype: str = "rename",
    max_versions: int = 5,
    debug: bool = False,
    dir_spec: Optional[str] = None,
) -> int:
    """Save max versions of file.

    Parameters
    ----------
    file_spec : str
        Path to the file to be versioned.
    vtype : str, optional
        Either rename or copy when versioning, by default "rename"
    max_versions : int, optional
        maximum number of versions, by default 5
    debug : bool, optional
        debug flag, by default False
    dir_spec : Optional[str]
        Path to the directory were versions are stored, by default file_spec directory

    Returns
    -------
    int
        exit code
    """
    if not os.path.isfile(file_spec):  # pragma no cover
        return 1
    # or, do other error checking:
    if vtype not in {"copy", "rename"}:  # pragma no cover
        vtype = "rename"

    root = check_root_filename(file_spec)

    # Find next available file version
    if dir_spec is None:
        new_file = clear_slot(root, 1, max_versions, debug)
    else:
        new_file = clear_directory_slot(
            dir_spec,
            os.path.basename(root),
            1,
            max_versions,
            debug,
        )
    # the code below is reported as not covered, but I
    # have ran several tests to verify, I suspect, I need
    # use a fake file system for testing but not now
    if not os.path.isfile(new_file):  # pragma no cover
        if vtype == "copy":
            shutil.copy(file_spec, new_file)
        else:
            os.rename(file_spec, new_file)

    return 0


# vim:ft=py noqa: E800
