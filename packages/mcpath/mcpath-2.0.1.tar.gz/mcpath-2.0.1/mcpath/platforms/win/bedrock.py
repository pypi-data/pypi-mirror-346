"""
Windows Bedrock Edition
"""

from os import path
from mcpath.facades import Bedrock
import os


class WinBedrockEdition(Bedrock):
    def _get_game_dir(self):
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        if path.isdir(p):
            return p
        return None

    def _get_logs_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        path_parts = game_dir.split(os.sep)
        if len(path_parts) > 2:
            p = path.join(os.sep.join(path_parts[:-2]), "logs")
            if path.isdir(p):
                return p
        return None

    def _get_executable(self):
        return "minecraft://"


def instance():
    return WinBedrockEdition()
