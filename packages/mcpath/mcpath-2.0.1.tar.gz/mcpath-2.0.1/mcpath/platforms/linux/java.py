"""
Linux Java Edition
"""

from os import path
from mcpath.facades import Java
from mcpath.utils import _get_latest_profile, _version_to_component
import os


class LinuxJavaEdition(Java):
    def _launch(self):
        path = self.get_launcher()
        if path:
            os.system(f'"{path}"')
        return path

    def _get_runtime(self, version):
        component, major_version = _version_to_component(version)
        if component is None:
            return "java"
        p = path.join(
            path.expanduser("~"),
            ".minecraft",
            "runtime",
            component,
            "linux",
            component,
            "bin",
            "java",
        )
        if path.isfile(p):
            return p
        return "java"

    def _get_launcher(self):
        p = path.join(
            path.expanduser("~"), ".minecraft", "launcher", "minecraft-launcher"
        )
        if path.isfile(p):
            return p
        return None

    def _get_game_dir(self):
        fp = path.join(path.expanduser("~"), ".minecraft", "launcher_profiles.json")
        p = _get_latest_profile(fp)
        if p and path.isdir(p):
            return p
        # fallback
        p = path.join(path.expanduser("~"), ".minecraft")
        if path.isdir(p):
            return p
        return None

    def _get_root_dir(self):
        p = path.join(path.expanduser("~"), ".minecraft")
        if path.isdir(p):
            return p
        return None


def instance():
    return LinuxJavaEdition()
