"""Top-level module for wtforglib Library."""

import platform
from inspect import stack
from typing import Tuple, Union

from wtforglib.functions import WINDOZE, windoze_not_implemented

if platform.system() != WINDOZE:
    from grp import getgrall, getgrgid  # noqa: WPS433
    from pwd import getpwnam, getpwuid  # noqa: WPS433


def get_user_name(uid: int) -> str:
    """Returns the user name of the user identified by uid.

    Parameters
    ----------
    uid : int
        User id

    Returns
    -------
    str
        User name
    """
    windoze_not_implemented(stack()[0][3])
    return getpwuid(uid)[0]


def get_user_groups(user: Union[str, int]) -> Tuple[str, ...]:
    """Returns a tuple of groups user belongs to.

    Parameters
    ----------
    user : Union[str, int]
        User name or uid

    Returns
    -------
    Tuple[str,...]
        Groups user belongs to
    """
    windoze_not_implemented(stack()[0][3])
    if isinstance(user, int):
        user_nm = get_user_name(int(user))
    else:
        user_nm = user
    groups = [gg.gr_name for gg in getgrall() if user_nm in gg.gr_mem]
    gid = getpwnam(user_nm).pw_gid
    groups.append(getgrgid(gid).gr_name)
    return tuple(groups)
