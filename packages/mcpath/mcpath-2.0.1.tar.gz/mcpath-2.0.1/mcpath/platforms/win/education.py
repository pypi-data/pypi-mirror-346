"""
Windows Education Edition
"""

from os import path
from mcpath.facades import Education


class WinEducationEdition(Education):
    def _get_game_dir(self):
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        if path.isdir(p):
            return p
        return None

    def _get_executable(self):
        return "minecraftEdu://"


def instance():
    return WinEducationEdition()
