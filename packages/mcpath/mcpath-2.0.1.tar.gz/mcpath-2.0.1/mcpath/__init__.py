"""
Get paths to Minecraft Java, Bedrock, Preview, and Education Edition folders.
"""

__all__ = ["java", "bedrock", "preview", "education", "platform"]
__version__ = "2.0.1"

from mcpath import facades
from mcpath.utils import platform, Proxy

java = Proxy("java", facades.Java)
bedrock = Proxy("bedrock", facades.Bedrock)
preview = Proxy("preview", facades.Preview)
education = Proxy("education", facades.Education)
