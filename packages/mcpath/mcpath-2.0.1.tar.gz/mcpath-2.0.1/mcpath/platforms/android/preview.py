"""
Android Preview Edition
"""

from mcpath.facades import Preview


class AndroidPreviewEdition(Preview): ...


def instance():
    return AndroidPreviewEdition()
