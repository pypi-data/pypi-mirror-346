"""
Windows Preview Edition
"""

from os import path
from mcpath.facades import Preview


class WinPreviewEdition(Preview):
    def _get_game_dir(self):
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        if path.isdir(p):
            return p
        return None

    def _get_executable(self):
        return "minecraft-preview://"


def instance():
    return WinPreviewEdition()
