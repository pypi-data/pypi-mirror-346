"""
iOS Java Edition
"""

from mcpath.facades import Java


class iOSJavaEdition(Java): ...


def instance():
    return iOSJavaEdition()
