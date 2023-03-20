import platform
import os
import subprocess
import shutil
import zipfile
import xml.etree.ElementTree as ET
import tempfile

is_win = platform.system() == 'Windows'
is_linux = platform.system() == 'Linux'
is_mac = platform.system() == 'Darwin'

linuxdeployqt_bin = 'tools/linuxdeployqt-6-x86_64.AppImage'
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

def get_binary_creator():
    if is_win:
        return get_ifw_path() + 'binarycreator.exe'
    
def get_repogen():
    if is_win:
        return get_ifw_path() + 'repogen.exe'

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

def generate_repos():
    # Generate repos
    print("> Updating the repositories...")

    shutil.rmtree(abs_path(ramses_common_repo))
    shutil.rmtree(abs_path(ramses_os_repo))
    shutil.rmtree(abs_path(ifw_repo))

    print(">> Ramses App")

    package_list = [
        'org.rxlaboratory.ramses.client',
        'org.rxlaboratory.ramses.client.app'
        ]

    if is_win:
        package_list = package_list + [
            'org.rxlaboratory.ramses.client.desktopShortcut',
            'org.rxlaboratory.ramses.client.startMenuShortcut'
        ]

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

    bin_args = [
        get_repogen(),
        '-p', 'packages',
        '-e', ','.join(package_list),
        '--compression', '9',
        abs_path(ramses_common_repo)
    ]

    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

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

    print(">> Update Updates.xml")

    xml_content = ""
    with open(ramses_os_repo + '/Updates.xml', 'r', encoding='utf8') as xml_file:
        xml_content = xml_file.read()

    new_xml = [
        '<RepositoryUpdate>',
        '<Repository action="add" url="../common" displayname="Ramses Common Components" />']
    if is_win:
        new_xml.append('<Repository action="add" url="../../ifw/win" displayname="RxLaboratory Maintenance Tool for Windows" />')
    new_xml.append('</RepositoryUpdate>')
    new_xml.append('</Updates>')

    xml_content = xml_content.replace('</Updates>','\n'.join(new_xml))

    with open(ramses_os_repo + '/Updates.xml', 'w', encoding='utf8') as xml_file:
        xml_file.write(xml_content)

    create_gitkeep(abs_path(ramses_os_repo))
    create_gitkeep(abs_path(ramses_common_repo))
    create_gitkeep(abs_path(ifw_repo))

    print(">> Done!")

def create_binaries():
    print("> Creating installer binaries...")

    offline_path = 'build/'
    online_path = 'build/'
    if is_win:
        offline_path = offline_path + 'Ramses_Offline-Installer.exe'
        online_path = online_path + 'Ramses_Online-Installer.exe'
    if is_linux:
        offline_path = offline_path + 'Ramses_Offline-Installer'
        online_path = online_path + 'Ramses_Online-Installer'
    if is_mac:
        offline_path = offline_path + 'Ramses_Offline-Installer'
        online_path = online_path + 'Ramses_Online-Installer'

    print(">> Offline...")

    bin_args = [
        get_binary_creator(),
        '-c', abs_path(config_file),
        '-p', abs_path('packages'),
        '--repository', abs_path(ramses_os_repo),
        '--repository', abs_path(ramses_common_repo),
        '--repository', abs_path(ifw_repo),
        '--compression', '9'
    ]

    if (is_mac):
        bin_args.append('-dmg')

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

    if (is_mac):
        bin_args.append('-dmg')

    bin_args.append( abs_path(online_path) )

    bin_process = subprocess.Popen( bin_args )
    bin_process.communicate()

    print(">> Done!")

    print("<< Finished! >>")

def export_client( appimage=True, deb=True):

    print("> Exporting Client")

    package_path = 'packages/org.rxlaboratory.ramses.client.app/'
    data_folder = os.path.join(package_path, 'data')
    meta_folder = os.path.join(package_path, 'meta')
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs('build/client/', exist_ok=True)

    if is_win:
        zip_file = 'build/client/ramses-client_' + version + '.zip'
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
                os.replace( 'Ramses-x86_64.AppImage', 'build/client/ramses-client_' + version + '-x86_64.AppImage' )

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
                    'build/client/ramses-client_' + version + '-amd64.deb'
                    )
                
                shutil.copytree( tmpdata_folder, '/home/duduf/Documents/test')

    print(">> Done!")

def export_maya():

    print("> Exporting Maya Add-on")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.addon.maya/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs('build/maya/', exist_ok=True)

    zip_file = 'build/maya/ramses-maya_' + version + '.zip'
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/maya/', zip)

    print(">> Done!")

def export_py():

    print("> Exporting Python API")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.dev.py/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs('build/py/', exist_ok=True)

    zip_file = 'build/py/ramses-py_' + version + '.zip'
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/py/', zip)

    print(">> Done!")

def export_server():

    print("> Exporting Server")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.server.standard/'
    version = get_version(package_path)

    print(">> Version: " + version)

    os.makedirs('build/server/', exist_ok=True)

    zip_file = 'build/server/ramses-server_' + version + '.zip'
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/ramses', zip)

    package_path = 'packages/org.rxlaboratory.ramses.server.docker-mysql/'
    zip_file = 'build/server/ramses-server_' + version + '_docker-mysql.zip'
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/docker-mysql', zip)

        package_path = 'packages/org.rxlaboratory.ramses.server.docker-sqlite/'
    zip_file = 'build/server/ramses-server_' + version + '_docker-sqlite.zip'
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip_dir(package_path + 'data/server/docker-sqlite', zip)

    print(">> Done!")

#prepare_os()
#deploy_client_app()
#generate_rcc()
#generate_repos()
#create_binaries()
export_client()
#export_maya()
#export_py()
#export_server()