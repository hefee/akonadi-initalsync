#! /bin/bash
# Script to test the initalsync on a docker image (debian jessie).
# Copyright: Sandro Knauß <knauss@kolabsys.com>
# License: GPL-2+
# Date: 2015-12-02

set -e
set -x

# Use same graphics system as host, since we'll share the X11 socket
export QT_GRAPHICSSYSTEM=native
export QT_X11_NO_MITSHM=1
# Give access to graphics card. Alternatively add user to group video
sudo setfacl -m user:developer:rw /dev/dri/card0

# Disable KCrash, so we can get a backtrace using gdb
export KDE_DEBUG=1

USER=doe
PASSWORD=Welcome2KolabSystems

sudo /usr/sbin/mysqld& >/tmp/mysql.log 2>/tmp/mysql.err
sleep 2

sudo mysql --defaults-extra-file=/etc/mysql/debian.cnf <<EOF
CREATE DATABASE $USER;
GRANT ALL  ON $USER.* TO '$USER'@localhost IDENTIFIED BY '$PASSWORD';
FLUSH PRIVILEGES;
EOF

./initalsync.py "John Doe" "doe@example.com" "$USER" "$PASSWORD" "akonadi_kolab_resource_0"
