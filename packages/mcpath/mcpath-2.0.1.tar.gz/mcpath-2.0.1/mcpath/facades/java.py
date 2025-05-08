"""
Supported Platforms
-------------------
Linux, MacOS, Windows
"""

__all__ = ["Java"]

from os import path

from ..utils import deprecated


class Java:
    """
    Java Edition facade.
    """

    def launch(self):
        """
        Launches Minecraft.
        """
        return self._launch()

    def get_runtime(self, version: str):
        """
        Get the path to the java runtime executable.
        """
        return self._get_runtime(version)

    def get_root_dir(self):
        """
        Get the path to the `.minecraft` folder.
        """
        return self._get_root_dir()

    def get_game_dir(self):
        """
        Get the path to the game directory.

        NOTE: If you want the `.minecraft` folder use get_root_dir instead.
        """
        return self._get_game_dir()

    def get_launcher(self):
        """
        Get the path to the Minecraft launcher.
        """
        return self._get_launcher()

    def get_versions_dir(self):
        """
        Get the path of the directory holding version jar files.
        """
        return self._get_versions_dir()

    def get_saves_dir(self):
        """
        Get the path of the directory holding world files.
        """
        return self._get_saves_dir()

    def get_resource_packs_dir(self):
        """
        Get the path of the directory holding resource pack files.
        """
        return self._get_resource_packs_dir()

    def get_screenshots_dir(self):
        """
        Get the path of the directory holding screenshot files.
        """
        return self._get_screenshots_dir()

    def get_backups_dir(self):
        """
        Get the path of the directory holding world backups.
        """
        return self._get_backups_dir()

    def get_logs_dir(self):
        """
        Get the path of the directory holding game log files.
        """
        return self._get_logs_dir()

    # backwards compatibility

    @property
    @deprecated
    def game(self):
        return self.get_game_dir()

    @property
    @deprecated
    def launcher(self):
        return self.get_launcher()

    @property
    @deprecated
    def executable(self):
        return self.get_versions_dir()

    @property
    @deprecated
    def worlds(self):
        return self.get_saves_dir()

    @property
    @deprecated
    def resource_packs(self):
        return self.get_resource_packs_dir()

    @property
    @deprecated
    def behavior_packs(self):
        return ""

    @property
    @deprecated
    def development_resource_packs(self):
        return self.get_resource_packs_dir()

    @property
    @deprecated
    def development_behavior_packs(self):
        return ""

    @property
    @deprecated
    def screenshots(self):
        return self.get_screenshots_dir()

    # private

    def _launch(self):
        return None

    def _get_runtime(self, version):
        return None

    def _get_root_dir(self):
        return None

    def _get_launcher(self):
        return None

    def _get_game_dir(self):
        return None

    def _get_versions_dir(self):
        root_dir = self.get_root_dir()
        if root_dir is None:
            return None
        return path.join(root_dir, "versions")

    def _get_saves_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        return path.join(game_dir, "saves")

    def _get_resource_packs_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        return path.join(game_dir, "resourcepacks")

    def _get_screenshots_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        return path.join(game_dir, "screenshots")

    def _get_backups_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        return path.join(game_dir, "backups")

    def _get_logs_dir(self):
        game_dir = self.get_game_dir()
        if game_dir is None:
            return None
        return path.join(game_dir, "logs")
