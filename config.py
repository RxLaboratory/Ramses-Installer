import os
from datetime import datetime
from pathlib import Path
import platform
from rxbuilder.utils import normpath

# General

RAMSES_MAIN_VERSION = '1.0.x' # TODO dynamic
RAMSES_PACKAGE_ID = 'org.rxlaboratory.ramses'
BUILD_DATE = datetime.today().strftime('%Y-%m-%d')
SYSTEM = platform.system()

REPO_PATH = normpath(Path(__file__).parent.resolve())
RAMSES_PARENT_PATH = normpath(Path(REPO_PATH).parent.resolve())
BUILD_PATH = os.path.join(REPO_PATH, 'build')
ASSETS_PATH = os.path.join(REPO_PATH, 'assets')

# RAMSES REPOS

RAMSES_MAYA_REPO = os.path.join(RAMSES_PARENT_PATH, "Ramses-Maya")
RAMSES_CLIENT_REPO = os.path.join(RAMSES_PARENT_PATH, "Ramses-Client")
RAMSES_PY_REPO = os.path.join(RAMSES_PARENT_PATH, "Ramses-Py")
RAMSES_SERVER_REPO = os.path.join(RAMSES_PARENT_PATH, "Ramses-Server")

# BIN CREATOR

BINARY_CREATOR = ''
if SYSTEM == 'Windows':
    f = 'C:/Qt/Tools/QtInstallerFramework/4.8/bin/binarycreator.exe'
    if os.path.isfile(f):
        BINARY_CREATOR = f
    f = 'C:/Qt/Tools/QtInstallerFramework/4.6/bin/binarycreator.exe'
    if os.path.isfile(f):
        BINARY_CREATOR = f
    f = 'C:/Qt/Tools/QtInstallerFramework/4.5/bin/binarycreator.exe'
    if os.path.isfile(f):
        BINARY_CREATOR = f

else:
    f = os.path.expanduser('~/Qt/Tools/QtInstallerFramework/4.8/bin/binarycreator')
    if os.path.isfile(f):
        BINARY_CREATOR = f
    f = os.path.expanduser('~/Qt/Tools/QtInstallerFramework/4.6/bin/binarycreator')
    if os.path.isfile(f):
        BINARY_CREATOR = f
    f = os.path.expanduser('~/Qt/Tools/QtInstallerFramework/4.5/bin/binarycreator')
    if os.path.isfile(f):
        BINARY_CREATOR = f
