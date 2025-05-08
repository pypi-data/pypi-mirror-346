"""
Android Education Edition
"""

from mcpath.facades import Education


# https://play.google.com/store/apps/details?id=com.mojang.minecraftedu
class AndroidEducationEdition(Education): ...


def instance():
    return AndroidEducationEdition()
