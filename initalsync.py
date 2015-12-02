#! /usr/bin/env python
#-*- coding: utf-8 -*-

""" Run a initial full sync of a akonadi resource.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2015-12-02
    Licence: GPL-2+
"""

import argparse
from email.Utils import formataddr
import logging
import os
import subprocess

from sync import akonadi, config, kwalletbinding
from sync.dbusServer import DBusServer

parser = argparse.ArgumentParser(description='run a initial full sync of a akonadi resource.')
parser.add_argument('name', help='name of the kolabuser')
parser.add_argument('mail', help='mail of the kolabuser')
parser.add_argument('uid', help='uid of the kolabuser')
parser.add_argument('password', help='password of the kolabuser')
parser.add_argument('resource', help='name of the akonadi_resource to sync something like "akonadi_kolab_resource_0"')

options = parser.parse_args()

name = options.name
email = options.mail
fullName = formataddr((name, email))
uid = options.uid
password =  options.password
home = os.path.expanduser("~")

akonadi_resource_name = options.resource

logging.basicConfig(level=logging.INFO)

logging.info("setup configs")
config.setupConfigDirs(home, fullName, email, name, uid, password)

with DBusServer():
	logging.info("set kwallet password")
	kwalletbinding.kwallet_put("imap", akonadi_resource_name+"rc", password)

	with akonadi.AkonadiServer(open("akonadi.log", "w"), open("akonadi.err", "w")):
            logging.info("trigger fullSync")
            akonadi.fullSync(akonadi_resource_name)

