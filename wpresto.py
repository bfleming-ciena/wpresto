import subprocess


# def create_container(cmd):
    # subprocess.check_call(cmd)

import os
# mk_db_vol_cmd = "docker run -d -v /var/lib/mysql --name dbdata busybox"
# os.system(mk_db_vol_cmd)

# mk_db_cmd = "docker run --volumes-from dbdata --name mysql -e MYSQL_ROOT_PASSWORD=admin -d mysql"
# os.system(mk_db_cmd)

# create_db = """docker run --volumes-from dbdata -v /Users/bfleming/Dropbox/Private-WordPress/tmp/wordpress-db.sql:/tmp/wordpress-db.sql -it --rm --link mysql:mysql mysql sh -c 'echo "create database wordpressdb;" | mysql -h $MYSQL_PORT_3306_TCP_ADDR -p'"""
# os.system(create_db)

# import_db_cmd = """docker run --volumes-from dbdata -v /Users/bfleming/Dropbox/Private-WordPress/tmp/wordpress-db.sql:/tmp/wordpress-db.sql -it --rm --link mysql:mysql mysql sh -c 'mysql -h $MYSQL_PORT_3306_TCP_ADDR -p wordpressdb < /tmp/wordpress-db.sql'"""
# os.system(import_db_cmd)
# # cmd_import_db = """docker exec -it mysql sh -c 'echo "create database wordpressdb;" | mysql -p; mysql -p wordpressdb < /tmp/wordpress-db.sql'"""


db_cmd = "docker run --name mysql  -v /Users/bfleming/Dropbox/Private-WordPress/stage/wordpress-db.sql:/tmp/wordpress-db.sql -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=wordpressdb -d mysql"
os.system(db_cmd)
print "    * Waiting for mysql server to come up..."
import time
time.sleep(10)
print "    * Importing database /tmp/wordpress-db.sql"
db_import_cmd = "docker exec mysql sh -c 'mysql --password=admin wordpressdb < /tmp/wordpress-db.sql'"
os.system(db_import_cmd)
# run_sql_cmd = "docker run --volumes-from dbdata --name mysql -e MYSQL_ROOT_PASSWORD=admin -d mysql"
# print cmd.split(" ")

# subprocess.check_call(cmd.split(" "))
