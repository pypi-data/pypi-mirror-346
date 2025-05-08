"""
Linux Education Edition
"""

from mcpath.facades import Education


class LinuxEducationEdition(Education): ...


def instance():
    return LinuxEducationEdition()
