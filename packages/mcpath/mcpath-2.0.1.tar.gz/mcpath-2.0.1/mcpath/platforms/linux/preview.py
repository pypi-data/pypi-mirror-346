"""
Linux Preview Edition
"""

from mcpath.facades import Preview


class LinuxPreviewEdition(Preview): ...


def instance():
    return LinuxPreviewEdition()
