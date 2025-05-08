"""
MacOS X Preview Edition
"""

from mcpath.facades import Preview


class OSXPreviewEdition(Preview): ...


def instance():
    return OSXPreviewEdition()
