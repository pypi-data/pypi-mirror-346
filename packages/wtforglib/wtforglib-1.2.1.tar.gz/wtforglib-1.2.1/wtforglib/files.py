"""Top-level module for wtforglib Library."""

import json
from pathlib import Path
from typing import Any

import yaml

from wtforglib.errors import raise_filenotfound
from wtforglib.kinds import Fspec, StrAnyDict

WRITE_YAML_DEPRECATED = (
    "WARNING: write_yaml_file is deprecated and will be removed "
    "in a future release. Use safe_write_yaml_file."
)


def load_yaml_file(
    file_spec: Fspec,
    missing_ok: bool = True,
) -> StrAnyDict:
    """Loads a yaml file.

    Parameters
    ----------
    file_spec : Fspec
        The yaml file to load
    missing_ok : bool optional default True
        When False and file does not exist raises FileNotFound exception

    Returns
    -------
    StrAnyDict
        Representing contents of file_spec
    """
    yaml_path = Path(file_spec)
    yaml_result = {}
    if yaml_path.exists() and yaml_path.is_file():
        with open(yaml_path, "r") as yaml_file:
            yaml_result = yaml.safe_load(yaml_file)
    elif not missing_ok:  # pragma no cover
        raise_filenotfound(yaml_path)
    return yaml_result


def safe_write_yaml_file(  # type: ignore [explicit-any]
    file_spec: Fspec, src_data: StrAnyDict, **kwargs: Any
) -> bool:
    """Writes src_data to a file in a yaml format.

    Parameters
    ----------
    file_spec : Fspec
        The yaml filename to write to
    src_data : StrAnyDict
        The data to write to a file
    kwargs : Optional
        Args passed to yaml.safe_dump

    Returns
    -------
        bool
            True if file exists else False
    """
    yaml_path = Path(file_spec)
    with open(yaml_path, "w") as out_file:
        yaml.safe_dump(src_data, out_file, **kwargs)
    return yaml_path.exists()


def write_yaml_file(
    file_spec: Fspec,
    src_data: StrAnyDict,
    encoding: str = "utf-8",
) -> bool:
    """Writes src_data to a file in a yaml format.

    Parameters
    ----------
    file_spec : Fspec
        The yaml filename to write to
    src_data : StrAnyDict
        The data to write to a file
    encoding : str Optional
        encoding default 'utf-8'

    Returns
    -------
        bool
            True if file exists else False
    """
    print(WRITE_YAML_DEPRECATED)  # noqa: WPS421
    yaml_path = Path(file_spec)
    with open(yaml_path, "w") as out_file:
        yaml.dump(src_data, out_file, encoding=encoding)
    return yaml_path.exists()


def load_json_file(
    file_spec: Fspec,
    missing_ok: bool = True,
) -> StrAnyDict:
    """Loads a json file.

    Parameters
    ----------
    file_spec : Fspec
        The yaml file to load
    missing_ok : bool optional default True
        When False and file does not exist raises FileNotFound exception

    Returns
    -------
    StrAnyDict
        Representing contents of file_spec
    """
    jpath = Path(file_spec)
    rtn: StrAnyDict = {}
    if jpath.exists() and jpath.is_file():
        with open(jpath, "r") as json_file:
            rtn = json.load(json_file)
    elif not missing_ok:  # pragma no cover
        raise_filenotfound(jpath)
    return rtn


def write_json_file(
    file_spec: Fspec,
    src_data: StrAnyDict,
    indent: int = 2,
) -> bool:
    """Writes src_data to a file in a json format.

    Parameters
    ----------
    file_spec : Fspec
        The json filename to write to
    src_data : StrAnyDict
        The data to write to a file
    indent : int Optional
        The number of spaces to indent

    Returns
    -------
        bool
            True if file exists else False
    """
    jpath = Path(file_spec)
    with open(jpath, "w") as out_file:
        out_file.write(json.dumps(src_data, indent=indent))
    return jpath.exists()
