import platform
import os
import subprocess
import shutil
import zipfile
import xml.etree.ElementTree as ET

is_win = platform.system() == 'Windows'
is_linux = platform.system() == 'Linux'
is_mac = platform.system() == 'Darwin'

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

def export_client():

    print("> Exporting Client")

    # Get the app version
    package_path = 'packages/org.rxlaboratory.ramses.client.app/'
    package_file = package_path + 'meta/package.xml'
    package_tree = ET.parse(package_file)
    root = package_tree.getroot()
    version = root.find('Version').text

    print(">> Version: " + version)

    os.makedirs('build/client/', exist_ok=True)

    if is_win:
        zip_file = 'build/client/ramses-client_' + version + '.zip'
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
            zip_dir(package_path + 'data/client/', zip)
            zip.write('packages/org.rxlaboratory.ramses.client/meta/license.md', 'License/license.md')
            zip.write('packages/org.rxlaboratory.ramses.client/meta/license.txt', 'License/license.txt')

    print(">> Done!")

def export_maya():

    print("> Exporting Maya Add-on")

    # Get the version
    package_path = 'packages/org.rxlaboratory.ramses.addon.maya/'
    package_file = package_path + 'meta/package.xml'
    package_tree = ET.parse(package_file)
    root = package_tree.getroot()
    version = root.find('Version').text

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
    package_file = package_path + 'meta/package.xml'
    package_tree = ET.parse(package_file)
    root = package_tree.getroot()
    version = root.find('Version').text

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
    package_file = package_path + 'meta/package.xml'
    package_tree = ET.parse(package_file)
    root = package_tree.getroot()
    version = root.find('Version').text

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

generate_rcc()
generate_repos()
create_binaries()
export_client()
export_maya()
export_py()
export_server()