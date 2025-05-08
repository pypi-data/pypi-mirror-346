# mcpath

![Tests](https://github.com/legopitstop/mcpath/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/mcpath)](https://pypi.org/project/mcpath/)
[![Python](https://img.shields.io/pypi/pyversions/mcpath)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcpath)
![Status](https://img.shields.io/pypi/status/mcpath)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcpath)](https://github.com/legopitstop/mcpath/issues)

Get paths to Minecraft Java, Bedrock, Preview, and Education Edition folders, launchers, executables and java runtime.

## Installation

Install the module with pip:

```bat
pip3 install mcpath
```

Update existing installation: `pip3 install mcpath --upgrade`

## Supported Platforms

|                   | Java     | Bedrock  | Preview/Beta | Education |
| ----------------- | -------- | -------- | ------------ | --------- |
| **Android** _[1]_ | ❌       | ✅       | ❌           | ❌        |
| **Darwin**        | ✅ _[3]_ | ❌       | ❌           | ❌        |
| **iOS** _[2]_     | ❌       | ✅       | ✅           | ✅        |
| **Linux**         | ✅       | ✅ _[4]_ | ❌           | ❌        |
| **Windows**       | ✅       | ✅       | ✅           | ✅        |

1. With [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&hl=en_US)
2. With [Pyto](https://apps.apple.com/us/app/pyto-ide/id1436650069)
3. Has not been tested.
4. With [mcpelauncher](https://mcpelauncher.readthedocs.io/en/latest/).

## Requirements

| Name                                                         | Usage                                                |
| ------------------------------------------------------------ | ---------------------------------------------------- |
| [`requests`](https://pypi.org/project/requests/)             | Get runtime component and version using Mojang's API |
| [`requests-cache`](https://pypi.org/project/requests-cache/) | For caching version data.                            |

## Examples

### Saves

```Python
import mcpath

print(mcpath.java.get_saves_dir())
# C:\Users\USER\AppData\Roaming\.minecraft\saves
```

### `.minecraft`

```Python
import mcpath

print(mcpath.java.get_root_dir())
# C:\Users\USER\AppData\Roaming\.minecraft
```

### Game

```Python
import mcpath

print(mcpath.java.get_game_dir())
# D:\minecraft
```

### Java Runtime Executable

```Python
import mcpath

print(mcpath.java.get_runtime('1.21.3'))
# C:\Users\USER\AppData\Local\Packages\Microsoft.4297127D64EC6_8wekyb3d8bbwe\LocalCache\Local\runtime\java-runtime-delta\windows-x64\java-runtime-delta\bin\java.exe
```
