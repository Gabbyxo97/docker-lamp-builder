from stat import S_IWUSR
from sys import argv
from git import Repo
from os import chmod, walk, remove, rmdir, path
from ymlfile import YMLFile


def rmtree(top):
    for root, dirs, files in walk(top, topdown=False):
        for name in files:
            filename = path.join(root, name)
            chmod(filename, S_IWUSR)
            remove(filename)
        for name in dirs:
            rmdir(path.join(root, name))
    rmdir(top)

def raw_input(prompt, default):
    return input(prompt) or default

def int_input(prompt, default):
    try:
        return int(input(prompt)) or default
    except ValueError:
        return default

if len(argv) < 2 or argv[1] == '':
    print('Usage: build [NAME]')
else:
    if argv[1] == 'build':
        if len(argv) < 3:
            print('Usage: build [NAME]')
        else:
            web_port = str(int_input('Website port (default: 80): ', 80))
            mysql_port = str(int_input('MySQL port (default: 3306): ', 3306))
            mysql_database = raw_input('MySQL database (default: [NAME]_db): ', argv[2] + '_db')
            mysql_user = raw_input('MySQL username (default: [NAME]): ', argv[2])
            mysql_password = raw_input('MySQL password (default: random password generated): ', '123')
            mysql_root_password = raw_input('MySQL root password (default: random password generated): ', '123')
            phpmyadmin_port = str(int_input('PHPMyAdmin port (default: 8000): ', 8000))

            Repo.clone_from('https://github.com/Gabbyxo97/docker-lamp.git', argv[2])
            rmtree(argv[2] + '/.git/')

            docker_compose = YMLFile(argv[2] + '/docker-compose.yml')
            docker_compose.obj['services']['www']['ports'] = [web_port + ':80']
            docker_compose.obj['services']['db']['ports'] = [mysql_port + ':3306']
            docker_compose.obj['services']['db']['environment']['MYSQL_DATABASE'] = mysql_database
            docker_compose.obj['services']['db']['environment']['MYSQL_USER'] = mysql_user
            docker_compose.obj['services']['db']['environment']['MYSQL_PASSWORD'] = mysql_password
            docker_compose.obj['services']['db']['environment']['MYSQL_ROOT_PASSWORD'] = mysql_root_password
            docker_compose.obj['services']['phpmyadmin']['ports'] = [phpmyadmin_port + ':80']
            docker_compose.obj['services']['phpmyadmin']['environment']['MYSQL_USER'] = mysql_user
            docker_compose.obj['services']['phpmyadmin']['environment']['MYSQL_PASSWORD'] = mysql_password
            docker_compose.obj['services']['phpmyadmin']['environment']['MYSQL_ROOT_PASSWORD'] = mysql_root_password
            docker_compose.save()

            print('Docker lamp project ' + argv[2] + ' made')
    if argv[1] == 'delete':
        if len(argv) < 3:
            print('Usage: delete [NAME]')
        else:
            rmtree(argv[2])

