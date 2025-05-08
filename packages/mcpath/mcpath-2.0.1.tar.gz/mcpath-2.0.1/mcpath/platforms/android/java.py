"""
Android Java Edition
"""

from mcpath.facades import Java


class AndroidJavaEdition(Java): ...


def instance():
    return AndroidJavaEdition()
