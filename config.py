import os
from datetime import datetime
from pathlib import Path
import platform
from rxbuilder.utils import normpath

# General

RAMSES_MAIN_VERSION = '1.0' # TODO dynamic
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
