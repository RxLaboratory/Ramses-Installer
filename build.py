import platform
import os
import subprocess
import shutil

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
        '<Repository action="add" url="common" displayname="Ramses Common Components" />']
    if is_win:
        new_xml.append('<Repository action="add" url="../ifw/win" displayname="RxLaboratory Maintenance Tool for Windows" />')
    new_xml.append('</RepositoryUpdate>')
    new_xml.append('</updates>')

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

#generate_rcc()
generate_repos()
create_binaries()