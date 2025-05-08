"""
Android Bedrock Edition
"""

from os import path
from mcpath.facades import Bedrock


class AndroidBedrockEdition(Bedrock):
    def _get_game_dir(self):
        internal = path.join(
            "data", "user", "0", "com.mojang.minecraftpe", "games", "com.mojang"
        )
        external = path.join(
            "storage",
            "emulated",
            "0",
            "Android",
            "data",
            "com.mojang.minecraftpe",
            "files",
            "games",
            "com.mojang",
        )
        if path.isdir(internal):
            return internal
        if path.isdir(external):
            return external
        return None

    def _get_executable(self):
        return "minecraft://"


def instance():
    return AndroidBedrockEdition()
