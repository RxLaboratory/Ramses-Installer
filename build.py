"""! @brief Builds the Ramses Installer with all packages
 @file build.py
 @section libs Librairies/Modules
 @section authors Author(s)
  - Created by Nicolas Dufresne on 9/19/2024 .
"""

import os
import shutil
import subprocess
from rxbuilder.utils import(
    wipe,
    replace_in_file,
    run_py,
    read_version,
    normpath
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
    BINARY_CREATOR
)

IFW_PATH = os.path.join(BUILD_PATH, 'ifw')
PACKAGES_PATH = os.path.join(IFW_PATH, 'packages')
CONFIG_PATH = os.path.join(IFW_PATH, 'config')

def copy_meta(package_name, version):
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
    xml_file = os.path.join(meta_path, "package.xml")
    # Update info
    replace_in_file(
            {
                '#version#': version,
                '#date#': BUILD_DATE
            },xml_file )
    return xml_file

def package_addons():
    # Copy meta
    copy_meta('addon', RAMSES_MAIN_VERSION)

def package_maya():

    # Build the maya addon
    build_script = os.path.join(RAMSES_MAYA_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    maya_mod_path = os.path.join(RAMSES_MAYA_REPO, 'build', 'ramses-maya')
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".addon.maya", 'data', 'maya')
    shutil.copytree(
        maya_mod_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_MAYA_REPO),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    copy_meta('addon.maya', version)

def package_client():
    # Copy meta
    copy_meta('client',RAMSES_MAIN_VERSION)

    # On Windows, add the shortcuts
    if SYSTEM == 'Windows':
        copy_meta('client.desktopShortcut',RAMSES_MAIN_VERSION)
        copy_meta('client.startMenuShortcut', RAMSES_MAIN_VERSION)

def package_client_app():

    # Build the client
    build_script = os.path.join(RAMSES_CLIENT_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    build_path = os.path.join(RAMSES_CLIENT_REPO, 'build', SYSTEM, 'deploy', 'Ramses' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".client.app", 'data')
    if SYSTEM == 'Windows':
        data_path = os.path.join(data_path, 'client')
    shutil.copytree(
        build_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_CLIENT_REPO),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    copy_meta('client.app', version)

def package_dev():
    # Copy meta
    copy_meta('dev',RAMSES_MAIN_VERSION)

def package_py():

    # Build the API
    build_script = os.path.join(RAMSES_PY_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    build_path = os.path.join(RAMSES_PY_REPO, 'build', 'ramses-py' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".dev.py", 'data', 'py')
    shutil.copytree(
        build_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_PY_REPO),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    copy_meta('dev.py', version)

def package_server():
    # Copy meta
    copy_meta('server',RAMSES_MAIN_VERSION)

def package_all_servers():

    # Build the Server
    build_script = os.path.join(RAMSES_SERVER_REPO, 'tools', 'deploy.py')
    run_py(build_script)

    # Copy the data
    build_path = os.path.join(RAMSES_SERVER_REPO, 'build', 'www' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".server.standard", 'data', 'server', 'ramses')
    shutil.copytree(
        build_path,
        data_path
    )
    build_path = os.path.join(RAMSES_SERVER_REPO, 'build', 'docker-mysql' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".server.docker-mysql", 'data', 'server', 'docker-mysql')
    shutil.copytree(
        build_path,
        data_path
    )
    build_path = os.path.join(RAMSES_SERVER_REPO, 'build', 'docker-sqlite' )
    data_path = os.path.join(PACKAGES_PATH, RAMSES_PACKAGE_ID+".server.docker-sqlite", 'data', 'server', 'docker-sqlite')
    shutil.copytree(
        build_path,
        data_path
    )

    # Get the version
    version = read_version(
        os.path.join(RAMSES_SERVER_REPO),
        RAMSES_MAIN_VERSION
    )

    # Copy meta
    copy_meta('server.standard', version)
    copy_meta('server.docker-mysql', version)
    copy_meta('server.docker-sqlite', version)

def package_all():
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
    package_server()
    package_all_servers()

def set_config():
    shutil.copytree(
        os.path.join(ASSETS_PATH, 'config' ),
        CONFIG_PATH
    )

    target_dir = "@HomeDir@/RxLaboratory/Ramses"
    run_program = "@TargetDir@/client/bin/ramses"
    admin_target_dir = "<AdminTargetDir>@ApplicationsDir@/RxLaboratory/Ramses</AdminTargetDir>"
    start_menu = ''
    if SYSTEM == 'Windows':
        target_dir = "@ApplicationsDir@/RxLaboratory/Ramses"
        run_program = "@TargetDir@/client/ramses"
        admin_target_dir = ""
        start_menu = "<StartMenuDir>Ramses</StartMenuDir>"
    elif SYSTEM == 'Darwin':
        target_dir = "@ApplicationsDir@/Ramses"
        run_program = "@TargetDir@/ramses.app/Contents/MacOS/Ramses"
        admin_target_dir = ""
        start_menu = ""


    config_file = os.path.join(CONFIG_PATH, 'config.xml')
    replace_in_file( {
        "#version#": RAMSES_MAIN_VERSION,
        "#targetdir#": target_dir,
        "#admintargetdir#": admin_target_dir,
        "#runprogram#": run_program,
        "#startmenu#": start_menu,
    }, config_file)

def create_binaries():
    print("Creating installer binaries...")
    if SYSTEM == 'Windows':
        bin_path = os.path.join( BUILD_PATH, 'Ramses-Installer_' + RAMSES_MAIN_VERSION + '_' + BUILD_DATE + '.exe' )
    elif SYSTEM == 'Linux':
        bin_path = os.path.join( BUILD_PATH, 'Ramses-Installer_' + RAMSES_MAIN_VERSION + '_' + BUILD_DATE )
    elif SYSTEM == 'Darwin':
        bin_path = os.path.join( BUILD_PATH, 'Ramses-Installer_' + RAMSES_MAIN_VERSION + '_' + BUILD_DATE + '.app' )

    bin_args = (
        BINARY_CREATOR,
        '-c', normpath(os.path.join(CONFIG_PATH, 'config.xml')),
        '-p', normpath(PACKAGES_PATH),
        '--compression', '9',
        bin_path
    )
    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

    if SYSTEM == 'Darwin':
        shutil.copy(
            os.path.join(CONFIG_PATH, 'ramses.icns'),
            os.path.join(bin_path, 'Contents/Resources/ramses-maintenancetool.icns')
        )
        replace_in_file({
            "</dict>": "\t<key>CFBundleIconFile</key>\n\t<string>ramses-maintenancetool.icns</string>\n</dict>"
            }, os.path.join(bin_path, 'Contents/Info.plist'))

        print("> Creating .dmg images...")
        dmg_file = bin_path.replace(".app", ".dmg")
        if os.path.isfile(dmg_file):
            os.remove(dmg_file)
        bin_args =[
            'hdiutil',
            'create',
            '-srcfolder', normpath(bin_path),
            normpath( dmg_file )
        ]
        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()

if __name__ == '__main__':
    package_all()
    set_config()
    create_binaries()
    print('>>> Done! <<<')



# TODO
# Install script remove previous installation
# maintenancetool.exe purge -c
# See https://stackoverflow.com/questions/46455360/workaround-for-qt-installer-framework-not-overwriting-existing-installation