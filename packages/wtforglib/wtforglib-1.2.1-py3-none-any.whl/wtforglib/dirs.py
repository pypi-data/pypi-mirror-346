"""Top-level module for wtforglib Library."""

import os
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryFile
from typing import Optional, Tuple

from wtforglib.kinds import Fspec


def ensure_directory(target: Fspec, perm: int = 0o755) -> bool:
    """Creates a directory if it doesn't exist.

    Parameters
    ----------
    target : Fspec
        The path to the target directory
    perm : int Optional
        The mode to use if creation needed

    Returns
    -------
    bool
        True if directory exists

    Raises
    ------
    NotADirectoryError
        if target exists, but not a directory
    """
    dp = Path(target)
    if dp.is_dir():
        return True
    if dp.exists():
        raise NotADirectoryError(
            'Pathname "{0}" is not a directory.'.format(str(target)),
        )
    dp.mkdir(mode=perm, parents=True)
    return True


def _verify_directory_write(dpath: Fspec) -> Optional[Exception]:
    """Verify that the given directory is writable.

    Parameters
    ----------
    dpath : Fspec
        Pathlike object specifying the directory

    Returns
    -------
    Optional[Exception]
        The exception when caught
    """
    error: Optional[Exception] = None
    try:
        temp_file = TemporaryFile(dir=dpath)
        temp_file.close()
    except Exception as ex:
        error = ex
    return error


def verify_directory(dspec: Fspec, ex: bool = False) -> Tuple[bool, str]:
    """Verify that a directory exits and is writable.

    Parameters
    ----------
    dspec : Fspec
        Pathlike object specifying the directory
    ex : bool, optional
        When True exceptions are raised, by default False

    Returns
    -------
    Tuple[bool, str]
        When ex is False the status is returned

    Raises
    ------
    error
        NotADirectoryError, FileNotFoundError or other exception is raised on failure
        when ex is True
    """
    dpath = Path(dspec)
    target_path_str = str(dpath)
    error: Optional[Exception]
    if dpath.exists():
        if dpath.is_dir():
            error = _verify_directory_write(dpath)
        else:
            error = NotADirectoryError(
                "'{0}' is not a directory".format(target_path_str),
            )
    else:
        error = FileNotFoundError("Directory not found: {0}".format(dpath))
    if error:
        if ex:
            raise error
    return error is None, str(error)


def delete_empty_dirs(path: Fspec) -> int:  # noqa: WPS210
    """Delete empty directories in the given path recursively.

    Parameters
    ----------
    path : Fspec
        The given path to walk through

    Returns
    -------
    int
        Number of directories deleted
    """
    removed = 0
    for root, dirs, _files in os.walk(path, topdown=False):
        for directory in dirs:
            dirpath = os.path.join(root, directory)
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
                removed += 1
    return removed


# function to perform delete operation based on condition
def prune_older_files(path: Fspec, max_days: int) -> int:  # noqa: WPS210
    """Delete files recursively in path if they are older than days.

    Parameters
    ----------
    path : Fspec
        Path to the folder to prune
    max_days : int
        Number of days to keep

    Returns
    -------
    int
        Number of files pruned
    """
    removed = 0
    # loop to check all files one by one
    # os.walk returns 3 things:
    #   - current path,
    #   - files in the current path, and
    #   - folders in the current path
    for root, _dirs, files in os.walk(path, topdown=True):
        for fn in files:
            # temp variable to store path of the file
            file_path = os.path.join(root, fn)
            # get the timestamp, when the file was modified
            timestamp_of_file_modified = os.path.getmtime(file_path)
            # convert timestamp to datetime
            modification_date = datetime.fromtimestamp(timestamp_of_file_modified)
            # find the number of days when the file was modified
            number_of_days = (datetime.now() - modification_date).days
            if number_of_days > max_days:
                # remove file
                os.remove(file_path)
                removed += 1
    return removed


def prune_older_files_empty_dir(path: Fspec, max_days: int) -> int:
    """Delete files recursively in path if they are older than days, delete empty dirs.

    Parameters
    ----------
    path : Fspec
        Path to the folder to prune
    max_days : int
        Number of days to keep

    Returns
    -------
    int
        Number of items removed
    """
    removed = prune_older_files(path, max_days)
    removed += delete_empty_dirs(path)
    return removed
