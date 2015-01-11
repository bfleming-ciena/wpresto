# from docker.client import Client
# from docker.utils import kwargs_from_env
# client = Client(**kwargs_from_env())

# print client.version()
# #

# import gzip
import sys
import argparse
import os.path

CONTAINERS = ["wordpress", "mysql", "dbdata", "webdata"]


# System call for unzip
def sys_unzip(afile, dest_dir="."):
    import subprocess
    try:
        subprocess.check_call(["gunzip", afile])
        return True
    except Exception:
        return False


# System call for unzip
def sys_untar(afile, dest_dir="."):
    import subprocess
    try:
        subprocess.check_call(["tar", "-xvf", afile, "-C", dest_dir])
        return True
    except Exception:
        return False

import fileinput
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def print_blue(s):
        print(bcolors.OKBLUE + s + bcolors.ENDC)

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

# Destroy the site
def perform_rm_arg():
    ans = raw_input('Permanent operation. Are you sure? (y/n) ')
    if 'y' not in ans:
        exit("abort.", 1)
    else:
        print("Removing related containers...")
        cmd = "docker rm -f " + " ".join(CONTAINERS)
        sysCmd(cmd)

# Short-hand
def exit(msg, code):
    print(msg if msg else "")
    sys.exit(code)

DEBUG=0
def sysCmd(cmd):
    if not DEBUG:
        os.system(cmd)
    else:
        print("DEBUG: %s" % (cmd))


blue = bcolors.print_blue

# Create an entire site from the BackWPup .tar.gz file. Nothing else needed!
def create_from_backup(filename):

        # Create DB Data Volume
        cmd='docker run -d -v /var/lib/mysql --name dbdata busybox echo "db data container"'
        blue("    [*] Creating DB data volume.")
        sysCmd(cmd)

        # Create Web Data Volume
        blue("    [*] Creating WP web data volume.")
        cmd='docker run -d -v /var/www/html --name webdata busybox echo "web data container"'
        sysCmd(cmd)

        # Create Wordpress container and link with the data volume
        abs_path = os.path.abspath(filename)
        name_part = os.path.basename(filename)
        blue("    [*] Creating MYSQL container and importing .sql file from %s" % (name_part))
        cmd = "docker run --name mysql --volumes-from dbdata -v %s:/tmp/%s -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=wordpressdb -e \
               MYSQL_BACKWPUP_TGZ=/tmp/%s -d mysqlwpresto" % (abs_path, name_part, name_part)
        sysCmd(cmd)

        import time
        blue("    [*] Creating WordPress container and importing %s" % (name_part))
        time.sleep(30)
        blue("    [*] Waiting a few seconds for MYSQL to come up...")
        cmd = "docker run --name wordpress --volumes-from webdata --link mysql:mysql -p 80:80 -d -e WORDPRESS_DB_NAME=wordpressdb \
              -e WORDPRESS_DB_PASSWORD=admin -v %s:/tmp/%s -e WORDPRESS_BACKWPUP_TGZ=/tmp/%s wordpresto" % (abs_path, name_part, name_part)
        sysCmd(cmd)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Create a Wordpress Site on Docker")
    parser.add_argument('--file', dest="filename", type=str)
    parser.add_argument('--rm', dest='remove', action='store_true')
    parser.add_argument('--launch', dest='launch', action='store_true') # assume vols exist?
    # parser.add_argument('--dest', dest="destdir", type=str)

    args = parser.parse_args()

    # Remove all traces of the site
    if args.remove:
        perform_rm_arg()

    # Create site from backup file option
    if args.filename:
        create_from_backup(args.filename)









    # parser.add_option("-q", "--quiet",
                      # action="store_false", dest="verbose", default=True,
                      # help="don't print status messages to stdout")
    #(options, args) = parser.parse_args()
    # tmp_file = "test.tar.gz"
    # shutil.copyfile(args.filename, tmp_file)
    # sys_unzip(tmp_file)

    # if os.path.isfile(options.filename):
        # sys_untar(options.filename, options.destdir)
        # print "DONE!"
    # print options.filename

    # replaceAll(options.destdir + "/wp-config.php", """/* That's all, stop editing! Happy blogging. */""", """define('RELOCATE',true)\n/* That's all, stop editing! Happy blogging. */""")

    # replaceAll(options.destdir + "/wp-config.php", """define('RELOCATE',true)\n""", "")


