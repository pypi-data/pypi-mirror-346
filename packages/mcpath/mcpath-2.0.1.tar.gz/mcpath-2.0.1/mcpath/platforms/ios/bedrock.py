"""
iOS Bedrock Edition
"""

from mcpath.facades import Bedrock
from mcpath.utils import _get_app


class iOSBedrockEdition(Bedrock):
    def _get_game_dir(self):
        app = _get_app()
        match app:
            case "pyto":
                import file_system

                while True:
                    p = file_system.pick_directory()
                    if p.endswith("games/com.mojang"):
                        return p
                    print("Invalid directory!")
            case "pythonista":
                # 1. Tap the hamburger menu at the top left
                # 2. Under "EXTERNAL FILES" tap "Open..."
                # 3. Then tap "Folder..."
                # 5. Navigate to your Minecraft folder and tap "Open"
                # 6. Finally, run the script again.
                ...
        raise PermissionError()

    def _get_executable(self):
        return "minecraft://"


def instance():
    return iOSBedrockEdition()
