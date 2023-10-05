import platform
import os
import subprocess
import shutil
import zipfile
import tarfile
import xml.etree.ElementTree as ET
import tempfile
import fnmatch

is_win = platform.system() == 'Windows'
is_linux = platform.system() == 'Linux'
is_mac = platform.system() == 'Darwin'

if is_mac:
    build_path = '/Users/duduf/RxLab/DEV/02 - Applications/Ramses/Export/'
if is_linux:
    build_path = '/home/duduf/RxLab/Dev/02 - Applications/Ramses/Export'
if is_win:
    build_path = 'd:\\RxLab\\Dev\\02 - Applications\\Ramses\\Export'

linuxdeployqt_bin = 'tools/linuxdeployqt-6-x86_64.AppImage'
macdeployqt_bin = '~/Qt/5.15.2/clang_64/bin/macdeployqt'
qmake_path = '~/Qt/5.12.5/gcc_64/bin/qmake'

this_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

config_file = 'config'
if is_win:
    config_file = os.path.join( config_file, 'config-win.xml' )
elif is_linux:
    config_file = os.path.join( config_file, 'config-linux.xml' )
elif is_mac:
    config_file = os.path.join( config_file, 'config-mac.xml' )

ramses_repo = 'repository/ramses/'
ramses_os_repo = ramses_repo
ifw_repo = 'repository/ifw'
ramses_common_repo = os.path.join(ramses_repo, 'common')
if is_win:
    ramses_os_repo = os.path.join(ramses_repo, 'win')
    ifw_repo = os.path.join(ifw_repo, 'win')
if is_linux:
    ramses_os_repo = os.path.join(ramses_repo, 'linux')
    ifw_repo = os.path.join(ifw_repo, 'linux')
if is_mac:
    ramses_os_repo = os.path.join(ramses_repo, 'mac')
    ifw_repo = os.path.join(ifw_repo, 'mac')

def get_ifw_path():
    if is_win:
        return 'C:/Qt/Tools/QtInstallerFramework/4.5/bin/'
    if is_linux or is_mac:
        return os.path.expanduser('~/Qt/Tools/QtInstallerFramework/4.5/bin/')

def get_binary_creator():
    if is_win:
        return get_ifw_path() + 'binarycreator.exe'
    if is_linux or is_mac:
        return get_ifw_path() + 'binarycreator'

def get_repogen():
    if is_win:
        return get_ifw_path() + 'repogen.exe'
    if is_linux or is_mac:
        return get_ifw_path() + 'repogen'

def abs_path( rel_path ):
    return os.path.abspath(
        os.path.join( this_dir, rel_path)
        ).replace('/', os.sep)

def create_gitkeep( dir ):
    with open(dir + '/.gitkeep', 'w') as f:
        pass

def zip_dir( dir, zip_file_handler ):
    for root, dirs, files in os.walk(dir):
        for file in files:
            zip_file_handler.write(os.path.join(root, file),
                                  os.path.join(root.replace(dir, ''), file)
                                  )

def get_version( package_path ):
    # Get the app version
    package_file = os.path.join( package_path, 'meta/package.xml' )
    package_tree = ET.parse(package_file)
    root = package_tree.getroot()
    version = root.find('Version').text
    return version

def replace_in_file( replacements, file ):
    lines = []
    with open( file ) as infile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            lines.append(line)
    with open( file , 'w') as outfile:
        for line in lines:
            outfile.write(line)

def get_dir_size( dir ):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def rename_to_lowercase( file ):
    if not os.path.isfile(file):
        return
    filename = os.path.basename(file)
    folder = os.path.dirname(file)
    filename_lower = filename.lower()
    file_lower = os.path.join( folder, filename_lower )
    # remove the lower case version
    if os.path.isfile( file_lower ):
        os.remove( file_lower )
    # rename
    os.rename( file, file_lower )

def prepare_os():
    for package in os.listdir('packages'):
        package_folder = os.path.join('packages', package)

        # Remove the current data folder and copy the os specific folder

        if not os.path.isdir(package_folder):
            continue
        data_folder_name = 'data'
        if is_win:
            data_folder_name = 'data-win'
        if is_linux:
            data_folder_name = 'data-linux'
        if is_mac:
            data_folder_name = 'data-mac'
        data_os_folder = os.path.join(package_folder, data_folder_name)
        if not os.path.isdir(data_os_folder):
            continue

        print("> Preparing data folder for current system (" + platform.system() + ") for package: " + package)

        data_folder = os.path.join(package_folder, 'data')
        if os.path.isdir(data_folder):
            shutil.rmtree( data_folder )

        shutil.copytree(data_os_folder, data_folder)

        print(">> Done!")

def deploy_client_app():
    package_folder = os.path.join('packages', 'org.rxlaboratory.ramses.client.app')
    data_folder = os.path.join(package_folder, 'data')

    print("> Deploying Client app...")

    # Deploy libs etc
    if is_win:
        # Manually copy files
        # TODO: windeplyqt + add libcrypto and other libs
        pass
    if is_linux:
        # Ramses bin should be lower case
        bin_folder = os.path.join(data_folder,'usr/bin')
        rename_to_lowercase( os.path.join(bin_folder, 'Ramses') )

        # Deploy using linuxdeployqt
        print(">> Deploying...")

        bin_args = [
            linuxdeployqt_bin,
            abs_path( os.path.join(data_folder, 'usr/share/applications/Ramses.desktop') ),
            '-unsupported-allow-new-glibc',
            '-always-overwrite',
            '-no-translations',
            '-qmake=' + os.path.expanduser(qmake_path),
            '-extra-plugins=iconengines,platformthemes/libqgtk3.so'
        ]

        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()
        
        # Rename the usr folder to "client"
        os.rename( os.path.join(data_folder, 'usr'), os.path.join(data_folder, 'client'))

        # Use a bigger icon!
        icon_file = os.path.join(data_folder, "ramses.png")
        if os.path.isfile(icon_file):
            os.remove(icon_file)
        shutil.copy( os.path.join(data_folder, 'client/share/icons/hicolor/128x128/apps/ramses.png'),
                    icon_file )
               
        # Remove the desktop file
        desktop_file = os.path.join(data_folder, 'Ramses.desktop')
        if os.path.isfile(desktop_file):
            os.remove(desktop_file)

    if is_mac:
        print(">> Deploying...")

        bin_args = [
            os.path.expanduser( macdeployqt_bin ),
            'Ramses.app'
        ]

        bin_process = subprocess.Popen( bin_args, cwd=abs_path(data_folder) )
        bin_process.communicate()

    print(">> Done!")

def generate_rcc():
    # Generate RCC
    print("> Generating .rcc file")

    print(">> Using config: " + config_file)

    bin_args = [
        get_binary_creator(),
        '-c', abs_path(config_file),
        '-p', abs_path('packages'),
        '-rcc'
    ]
    bin_process = subprocess.Popen(
        bin_args,
        cwd=abs_path('packages/org.rxlaboratory.ifw.maintenancetool/data')
        )

    bin_process.communicate()
    # print(">> " + str(output[1]))
    print(">> Done!")

def generate_repos( common_only=False ):
    # Generate repos
    print("> Updating the repositories...")

    shutil.rmtree(abs_path(ramses_common_repo))
    if not common_only:
        shutil.rmtree(abs_path(ramses_os_repo))
        shutil.rmtree(abs_path(ifw_repo))

    package_list = [
        'org.rxlaboratory.ramses.client',
        'org.rxlaboratory.ramses.client.app'
        ]
    if is_win:
        package_list = package_list + [
            'org.rxlaboratory.ramses.client.desktopShortcut',
            'org.rxlaboratory.ramses.client.startMenuShortcut'
        ]

    if not common_only:
        print(">> Ramses App")

        bin_args = [
            get_repogen(),
            '-p', 'packages',
            '-i', ','.join(package_list),
            '--compression', '9',
            abs_path(ramses_os_repo)
        ]

        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()

    print(">> Ramses Common Components")
    package_list.append( 'org.rxlaboratory.ifw.maintenancetool' )
    if not is_win:
        package_list = package_list + [
            'org.rxlaboratory.ramses.client.desktopShortcut',
            'org.rxlaboratory.ramses.client.startMenuShortcut'
        ]

    bin_args = [
        get_repogen(),
        '-p', 'packages',
        '-e', ','.join(package_list),
        '--compression', '9',
        abs_path(ramses_common_repo)
    ]

    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

    if not common_only:
        print(">> Maintenance Tool")

        bin_args = [
            get_repogen(),
            '-p', 'packages',
            '-i', 'org.rxlaboratory.ifw.maintenancetool',
            '--compression', '9',
            abs_path(ifw_repo)
        ]

        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()

    if not common_only:
        print(">> Update Updates.xml")
        xml_content = ""
        with open(ramses_os_repo + '/Updates.xml', 'r', encoding='utf8') as xml_file:
            xml_content = xml_file.read()

        new_xml = [
            '<RepositoryUpdate>',
            '<Repository action="add" url="../common" displayname="Ramses Common Components" />'
            ]
        if is_win:
            new_xml.append('<Repository action="add" url="../../ifw/win" displayname="RxLaboratory Maintenance Tool for Windows" />')
        new_xml.append('</RepositoryUpdate>')
        new_xml.append('</Updates>')

        xml_content = xml_content.replace('</Updates>','\n'.join(new_xml))

        with open(ramses_os_repo + '/Updates.xml', 'w', encoding='utf8') as xml_file:
            xml_file.write(xml_content)

        create_gitkeep(abs_path(ramses_os_repo))
        create_gitkeep(abs_path(ifw_repo))

    create_gitkeep(abs_path(ramses_common_repo))

    print(">> Done!")

def create_binaries():
    print("> Creating installer binaries...")

    offline_path = build_path
    online_path = build_path
    if is_win:
        offline_path = os.path.join( offline_path, 'Ramses_Offline-Installer.exe' )
        online_path = os.path.join( online_path, 'Ramses_Online-Installer.exe')
    if is_linux:
        offline_path = os.path.join( offline_path, 'Ramses_Offline-Installer')
        online_path = os.path.join( online_path, 'Ramses_Online-Installer')
    if is_mac:
        offline_path = os.path.join( offline_path, 'Ramses_Offline-Installer.app')
        online_path = os.path.join( online_path, 'Ramses_Online-Installer.app')

    print(">> Offline...")

    print(">>> OS Specific Repo path: " + abs_path(ramses_os_repo))
    print(">>> Common Repo path: " + abs_path(ramses_common_repo))
    print(">>> IFW Repo path: " + abs_path(ifw_repo))

    bin_args = [
        get_binary_creator(),
        '-c', abs_path(config_file),
        '-p', abs_path('packages'),
        '--repository', abs_path(ramses_os_repo),
        '--repository', abs_path(ramses_common_repo),
        '--repository', abs_path(ifw_repo),
        '--compression', '9'
    ]

    bin_args.append( abs_path(offline_path) )

    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

    print(">> Online...")

    bin_args = [
        get_binary_creator(),
        '-c', abs_path(config_file),
        '-p', abs_path('packages'),
        '--online-only'
    ]

    bin_args.append( abs_path(online_path) )

    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

    if is_mac:
        print(">> Setting icon...")
        shutil.copy(
            'config/ramses-maintenancetool.icns',
            os.path.join(online_path, 'Contents/Resources/ramses-maintenancetool.icns')
        )
        shutil.copy(
            'config/ramses-maintenancetool.icns',
            os.path.join(offline_path, 'Contents/Resources/ramses-maintenancetool.icns')
        )
        replace_in_file(
            {"</dict>": "\t<key>CFBundleIconFile</key>\n\t<string>ramses-maintenancetool.icns</string>\n</dict>"},
            os.path.join(offline_path, 'Contents/Info.plist')
        )
        replace_in_file(
            {"</dict>": "\t<key>CFBundleIconFile</key>\n\t<string>ramses-maintenancetool.icns</string>\n</dict>"},
            os.path.join(online_path, 'Contents/Info.plist')
        )
        print(">> Creating .dmg images...")
        offline_dmg = offline_path.replace(".app", ".dmg")
        online_dmg = online_path.replace(".app", ".dmg")
        if os.path.isfile(offline_dmg):
            os.remove(offline_dmg)
        if os.path.isfile(online_dmg):
            os.remove(online_dmg)
        bin_args =[
            'hdiutil',
            'create',
            '-srcfolder', abs_path(online_path),
            abs_path( online_path.replace(".app", ".dmg"))
        ]
        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()
        bin_args =[
            'hdiutil',
            'create',
            '-srcfolder', abs_path(offline_path),
            abs_path( offline_path.replace(".app", ".dmg"))
        ]
        bin_process = subprocess.Popen( bin_args )
        bin_process.communicate()

        shutil.rmtree( online_path )
        shutil.rmtree( offline_path )

    print(">> Done!")

def export_client( appimage=True, deb=True, tgz=True):

    print("> Exporting Client")

    package_path = 'packages/org.rxlaboratory.ramses.client.app/'
    data_folder = os.path.join(package_path, 'data')
    meta_folder = os.path.join(package_path, 'meta')
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs(os.path.join(build_path, 'client/'), exist_ok=True)

    if is_win:
        zip_file = os.path.join(build_path, 'client/ramses-client_' + version + '.zip')
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
            zip_dir(package_path + 'data/client/', zip)
            zip.write('packages/org.rxlaboratory.ramses.client/meta/license.md', 'License/license.md')
            zip.write('packages/org.rxlaboratory.ramses.client/meta/license.txt', 'License/license.txt')

    if is_linux:
        # Build AppImage
        # in a temp folder
        if appimage:
            print(">> Exporting .AppImage...")
            with tempfile.TemporaryDirectory() as tmpdata_folder:
                print(">> Creating temp data in " + tmpdata_folder)

                # AppRun may cause problems
                apprun = os.path.join(data_folder, 'AppRun')
                try:
                    os.remove( apprun )
                except:
                    pass

                # copy data to the tmpfolder
                shutil.rmtree( tmpdata_folder )
                shutil.copytree( data_folder, tmpdata_folder)

                # Rename "client" to "usr"
                if os.path.isdir( os.path.join(tmpdata_folder, 'client')):
                    os.rename(
                        os.path.join(tmpdata_folder, 'client'),
                        os.path.join(tmpdata_folder, 'usr')
                    )

                bin_args = [
                    linuxdeployqt_bin,
                    abs_path( os.path.join(tmpdata_folder, 'usr/share/applications/Ramses.desktop') ),
                    '-unsupported-allow-new-glibc',
                    '-appimage',
                    '-always-overwrite',
                    '-no-translations',
                    '-qmake=' + os.path.expanduser(qmake_path),
                    '-extra-plugins=iconengines,platformthemes/libqgtk3.so'
                ]

                bin_process = subprocess.Popen( bin_args )
                bin_process.communicate()

                # Move the Appimage to the build folder
                for f in os.listdir():
                    if f.startswith('Ramses') and f.endswith('x86_64.AppImage'):
                        shutil.copyfile(f, os.path.join(
                                build_path,
                                'client/ramses-client_' + version + '-x86_64.AppImage'
                                ))
                        os.remove(f)
                        break

        # Build .deb
        # in a temp folder
        if deb:
            print(">> Exporting .deb...")
            with tempfile.TemporaryDirectory() as tmpdata_folder:
                print(">> Creating temp data in " + tmpdata_folder)

                linux_data_folder = os.path.join(package_path, 'data-linux')

                # copy data to the tmpfolder
                deb_folder = os.path.join(tmpdata_folder, 'deb')
                shutil.copytree( linux_data_folder, deb_folder)

                rename_to_lowercase( os.path.join(deb_folder, 'usr/bin/Ramses') )

                # Create DEBIAN folder
                debian_folder = os.path.join(deb_folder, "DEBIAN")

                os.mkdir( debian_folder )
                shutil.copy(
                    os.path.join(meta_folder, 'copyright'),
                    os.path.join(debian_folder, 'copyright')
                    )
                control_file = os.path.join(debian_folder, 'control')
                shutil.copy(
                    os.path.join(meta_folder, 'control'),
                    control_file
                    )
                # Update control file
                size = get_dir_size( linux_data_folder )
                size = round( size / 1024 )
                replace_in_file( {
                        "#version#": version,
                        "#size#": str(size)
                        },
                        control_file
                    )
                               
                cmd_str = "find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '%P ' | xargs md5sum > DEBIAN/md5sums"
                subprocess.run(cmd_str, shell=True, cwd=abs_path(deb_folder))
                subprocess.run("chmod 755 DEBIAN", shell=True, cwd=abs_path(deb_folder))
                subprocess.run("dpkg -b deb ramses.deb", shell=True, cwd=abs_path(tmpdata_folder))

                # Get the result
                shutil.copy(
                    os.path.join(tmpdata_folder, 'ramses.deb'),
                    os.path.join(build_path, 'client/ramses-client_' + version + '-amd64.deb' )
                    )

        # Generate tgz  
        if tgz:
            print(">> Exporting .tar.gz...")
            client_path = os.path.join(data_folder, 'client')
            with tarfile.open( os.path.join(build_path, 'client/ramses-client_' + version + '.tar.gz') , "w:gz") as tar:
                for filename in os.listdir(client_path):
                    p = os.path.join(client_path, filename)
                    tar.add(p, arcname=filename)

    if is_mac:
        print(">> Exporting .dmg...")
        # Generate a dmg
        bin_args = [
            os.path.expanduser( macdeployqt_bin ),
            'Ramses.app', '-dmg'
        ]

        bin_process = subprocess.Popen( bin_args, cwd=abs_path(data_folder) )
        bin_process.communicate()

        os.rename(
            os.path.join(data_folder, 'Ramses.dmg'),
            os.path.join(build_path, 'client/ramses-client_' + version + '.dmg')
            )

    print(">> Done!")

def export_maya():

    print("> Exporting Maya Add-on")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.addon.maya/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs( os.path.join(build_path, 'maya/'), exist_ok=True)

    zip_file = os.path.join(build_path, 'maya/ramses-maya_' + version + '.zip' )
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/maya/', zip)

    print(">> Done!")

def export_py():

    print("> Exporting Python API")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.dev.py/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs(os.path.join(build_path, 'py/' ), exist_ok=True)

    zip_file = os.path.join(build_path, 'py/ramses-py_' + version + '.zip' )
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/py/', zip)

    print(">> Done!")

def export_server():

    print("> Exporting Server")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.server.standard/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs(os.path.join(build_path, 'server/' ), exist_ok=True)

    zip_file = os.path.join(build_path, 'server/ramses-server_' + version + '.zip' )
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/ramses', zip)

    package_path = 'packages/org.rxlaboratory.ramses.server.docker-mysql/'
    zip_file = os.path.join(build_path, 'server/ramses-server_' + version + '_docker-mysql.zip' )
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/docker-mysql', zip)

        package_path = 'packages/org.rxlaboratory.ramses.server.docker-sqlite/'
    zip_file = os.path.join(build_path, 'server/ramses-server_' + version + '_docker-sqlite.zip' )
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/docker-sqlite', zip)

    print(">> Done!")

def remove_sync_conflicts():

    print("> Removing sync conflicts")

    # In this dir
    print(">> In: " + this_dir)
    for root, dirs, files in os.walk(this_dir):
        for name in files:
            if fnmatch.fnmatch(name, '*sync-conflict*'):
                print(">>> Removing: " + name)
                os.remove(os.path.join(root, name))

    # In exports
    print(">> In: " + build_path)     
    for root, dirs, files in os.walk(build_path):
        for name in files:
            if fnmatch.fnmatch(name, '*sync-conflict*'):
                print(">>> Removing: " + name)
                os.remove(os.path.join(root, name))

def build_all():
    "Builds and exports everything"
    remove_sync_conflicts()
    prepare_os()
    deploy_client_app()
    generate_rcc()
    generate_repos()
    create_binaries()
    export_client()
    export_maya()
    export_py()
    export_server()
    remove_sync_conflicts()

def build_common_packages():
    """Builds and exports only the common packages and repos"""
    remove_sync_conflicts()
    generate_repos(True)
    export_maya()
    export_py()
    export_server()
    remove_sync_conflicts()

create_binaries()
#build_common_packages()

print("<< Finished! >>")
