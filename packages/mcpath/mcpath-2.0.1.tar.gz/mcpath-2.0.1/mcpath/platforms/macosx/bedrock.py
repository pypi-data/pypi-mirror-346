"""
MacOS X Bedrock Edition
"""

from mcpath.facades import Bedrock


class OSXBedrockEdition(Bedrock): ...


def instance():
    return OSXBedrockEdition()
