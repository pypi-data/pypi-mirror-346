"""
MacOS X Education Edition
"""

from mcpath.facades import Education


class OSXEducationEdition(Education): ...


def instance():
    return OSXEducationEdition()
