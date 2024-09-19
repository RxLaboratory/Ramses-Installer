"""! @brief Builds the Ramses Installer with all packages
 @file build.py
 @section libs Librairies/Modules
 @section authors Author(s)
  - Created by Nicolas Dufresne on 9/19/2024 .
"""

import os
import shutil
from rxbuilder.utils import(
    wipe,
    replace_in_file,
    run_py,
    read_version
)
from config import (
    RAMSES_MAIN_VERSION,
    BUILD_PATH,
    RAMSES_PACKAGE_ID,
    ASSETS_PATH,
    BUILD_DATE,
    RAMSES_MAYA_REPO,
    RAMSES_CLIENT_REPO,
    RAMSES_PY_REPO,
    RAMSES_SERVER_REPO,
    SYSTEM,
)

PACKAGES_PATH = os.path.join(BUILD_PATH, 'packages')

def copy_meta(package_name):
    src_path = os.path.join(ASSETS_PATH, 'meta', package_name)
    meta_path = os.path.join(
        PACKAGES_PATH,
        RAMSES_PACKAGE_ID+'.'+package_name,
        'meta'
        )
    #os.makedirs( meta_path )
    shutil.copytree(
        src_path,
        meta_path
    )
    return os.path.join(meta_path, "package.xml")

def package_addons():
    # Copy meta
    xml_file = copy_meta('addon')
    # Update info
    replace_in_file(
        (
            { 
                '#version#': RAMSES_MAIN_VERSION,
                '#date#': BUILD_DATE
            }
        ),
        xml_file
    )

def package_maya():

    # Build the maya addon
    build_script = os.path.join(RAMSES_MAYA_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    maya_mod_path = os.path.join(RAMSES_MAYA_REPO, 'build', 'ramses-maya')
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".addon.maya", 'data')
    shutil.copytree(
        maya_mod_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_MAYA_REPO, 'build'),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    xml_file = copy_meta('addon.maya')
    # Update info
    replace_in_file(
        (
            { 
                '#version#': version,
                '#date#': BUILD_DATE
            }
        ),
        xml_file
    )

def package_client():
    # Copy meta
    xml_file = copy_meta('client')
    # Update info
    replace_in_file(
        (
            { 
                '#version#': RAMSES_MAIN_VERSION,
                '#date#': BUILD_DATE
            }
        ),
        xml_file
    )

    # On Windows, add the shortcuts
    if SYSTEM == 'Windows':
        # Copy meta
        xml_file = copy_meta('client.desktopShortcut')
        # Update info
        replace_in_file(
            (
                { 
                    '#version#': RAMSES_MAIN_VERSION,
                    '#date#': BUILD_DATE
                }
            ),
            xml_file
        )
        # Copy meta
        xml_file = copy_meta('client.startMenuShortcut')
        # Update info
        replace_in_file(
            (
                { 
                    '#version#': RAMSES_MAIN_VERSION,
                    '#date#': BUILD_DATE
                }
            ),
            xml_file
        )

def package_client_app():

    # Build the client
    build_script = os.path.join(RAMSES_CLIENT_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    build_path = os.path.join(RAMSES_CLIENT_REPO, 'build', SYSTEM, 'deploy', 'Ramses' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".client.app", 'data')
    shutil.copytree(
        build_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_CLIENT_REPO, 'build', SYSTEM),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    xml_file = copy_meta('client.app')
    # Update info
    replace_in_file(
        (
            { 
                '#version#': version,
                '#date#': BUILD_DATE
            }
        ),
        xml_file
    )

def package_dev():
    # Copy meta
    xml_file = copy_meta('dev')
    # Update info
    replace_in_file(
        (
            { 
                '#version#': RAMSES_MAIN_VERSION,
                '#date#': BUILD_DATE
            }
        ),
        xml_file
    )

def package_py():
    pass

def package_all():

    # TODO data subfolders in packages!
    wipe(BUILD_PATH)
    print('Packaging Add-ons...')
    package_addons()
    print('Packaging Maya Add-on...')
    package_maya()
    print('Packaging Client...')
    package_client()
    package_client_app()
    package_dev()
    package_py()
    # server
    # docker mysal
    # docker sqlite
    # standard

# def build/config/

# def binarycreator

if __name__ == '__main__':
    package_all()
