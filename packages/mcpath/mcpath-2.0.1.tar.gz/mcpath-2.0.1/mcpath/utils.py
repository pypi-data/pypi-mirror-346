__all__ = [
    "Platform",
    "Proxy",
    "platform",
    "deprecated",
    "_version_to_component",
    "_get_latest_profile",
    "_get_version_manifest",
    "_get_app",
]

from typing import Union, Tuple, Callable, TypeVar
from os import environ
from sys import platform as _sys_platform
import os
import datetime
import json
import requests
import sys
import functools
import requests_cache
import warnings

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

_session = requests_cache.CachedSession()


@functools.lru_cache()
def _version_to_component(mcversion) -> Union[Tuple[str, int], Tuple[None, None]]:
    for version in _get_version_manifest()["versions"]:
        if version["id"] == mcversion:
            res = _session.get(version["url"])
            if not res.ok:
                return None, None
            package = res.json()
            if "javaVersion" not in package:
                return None, None
            return (
                package["javaVersion"]["component"],
                package["javaVersion"]["majorVersion"],
            )
    return None, None


MANIFEST_CACHE = None


def _get_version_manifest():
    global MANIFEST_CACHE
    if not MANIFEST_CACHE:
        res = requests.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        )
        if not res.ok:
            return None
        MANIFEST_CACHE = res.json()
    return MANIFEST_CACHE


def _get_latest_profile(fp) -> Union[str, None]:
    if os.path.exists(fp):
        with open(fp) as fd:
            profiles = json.load(fd)
        latest = None
        for profile in profiles.get("profiles", {}).values():
            timestamp = datetime.datetime.strptime(
                profile.get("lastUsed"), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if latest is None or timestamp > latest.get("timestamp"):
                profile["timestamp"] = timestamp
                latest = profile
        if latest and "gameDir" in latest:
            return str(latest["gameDir"])
    return None


def _get_app():
    """
    Get the Python app thats running this script.
    """
    try:
        import appex  # Pythonista module

        return "pythonista"
    except ImportError:
        ...
    try:
        import pyto_ui  # Pyto module

        return "pyto"
    except ImportError:
        ...
    raise NotImplementedError()


# From: https://github.com/kivy/plyer/blob/master/plyer/utils.py
class Platform:
    """
    Refactored to class to allow module function to be replaced
    with module variable.
    """

    def __init__(self):
        self._platform_ios = None
        self._platform_android = None

    def __eq__(self, other):
        return other == self._get_platform()

    def __ne__(self, other):
        return other != self._get_platform()

    def __str__(self):
        return self._get_platform()

    def __repr__(self):
        return "platform name: '{platform}' from: \n{instance}".format(
            platform=self._get_platform(), instance=super().__repr__()
        )

    def __hash__(self):
        return self._get_platform().__hash__()

    def _get_platform(self):

        if self._platform_android is None:
            # sys.getandroidapilevel is defined as of Python 3.7
            # ANDROID_ARGUMENT and ANDROID_PRIVATE are 2 environment variables
            # from python-for-android project
            self._platform_android = (
                hasattr(sys, "getandroidapilevel") or "ANDROID_ARGUMENT" in environ
            )

        # Modified to check for ios and ipados
        if self._platform_ios is None:
            self._platform_ios = (
                _sys_platform.lower() in ["ios", "ipados"]
                or environ.get("KIVY_BUILD", "") == "ios"
            )

        # On android, _sys_platform return 'linux2', so prefer to check the
        # import of Android module than trying to rely on _sys_platform.

        if self._platform_android is True:
            return "android"
        elif self._platform_ios is True:
            return "ios"
        elif _sys_platform in ("win32", "cygwin"):
            return "win"
        elif _sys_platform == "darwin":
            return "macosx"
        elif _sys_platform[:5] == "linux":
            return "linux"
        return "unknown"


platform = Platform()


# From: https://github.com/kivy/plyer/blob/master/plyer/utils.py
class Proxy:
    """
    Based on http://code.activestate.com/recipes/496741-object-proxying
    version by Tomer Filiba, PSF license.
    """

    __slots__ = ["_obj", "_name", "_facade"]

    def __init__(self, name, facade):
        object.__init__(self)
        object.__setattr__(self, "_obj", None)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_facade", facade)

    def _ensure_obj(self):
        obj = object.__getattribute__(self, "_obj")
        if obj:
            return obj
        # do the import
        try:
            name = object.__getattribute__(self, "_name")
            module = "mcpath.platforms.{}.{}".format(platform, name)
            mod = __import__(module, fromlist=".")
            obj = mod.instance()
        except Exception:
            import traceback

            traceback.print_exc()
            facade = object.__getattribute__(self, "_facade")
            obj = facade()

        object.__setattr__(self, "_obj", obj)
        return obj

    def __getattribute__(self, name):
        result = None

        if name == "__doc__":
            return result

        # run _ensure_obj func, result in _obj
        object.__getattribute__(self, "_ensure_obj")()

        # return either Proxy instance or platform-dependent implementation
        result = getattr(object.__getattribute__(self, "_obj"), name)
        return result

    def __delattr__(self, name):
        object.__getattribute__(self, "_ensure_obj")()
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value):
        object.__getattribute__(self, "_ensure_obj")()
        setattr(object.__getattribute__(self, "_obj"), name, value)

    def __bool__(self):
        object.__getattribute__(self, "_ensure_obj")()
        return bool(object.__getattribute__(self, "_obj"))

    def __str__(self):
        object.__getattribute__(self, "_ensure_obj")()
        return str(object.__getattribute__(self, "_obj"))

    def __repr__(self):
        object.__getattribute__(self, "_ensure_obj")()
        return repr(object.__getattribute__(self, "_obj"))


rT = TypeVar("rT")
pT = ParamSpec("pT")


def deprecated(func: Callable[pT, rT]) -> Callable[pT, rT]:
    """Use this decorator to mark functions as deprecated.
    Every time the decorated function runs, it will emit
    a "deprecation" warning."""

    @functools.wraps(func)
    def new_func(*args: pT.args, **kwargs: pT.kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to a deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func
