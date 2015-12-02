#-*- coding: utf-8 -*-

""" Handle a DBusServer

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2015-12-02
    Licence: GPL-2+
"""

import os, signal
import subprocess

import logging

logger = logging.getLogger("DBusServer")

class DBusServer():
	"""starts/stops a dbus server, if non is running with enter/exit the with statement."""
	def __init__(self):
	    self.startOwnServer = False
            self.environ = {}

        def __enter__(self):
	    if not self.running():
               self.start()
	    return self

        def __exit__(self, type, value, traceback):
            if self.startOwnServer:
               self.stop()

	def running(self):
	    return os.environ.has_key("DBUS_SESSION_BUS_ADDRESS")

	def start(self):
	    logger.info("starting dbus...")
	    p = subprocess.Popen('dbus-launch', shell=True, stdout=subprocess.PIPE)
	    for var in p.stdout:
		sp = var.strip().split('=', 1)
		self.environ[sp[0]] = os.environ.get(sp[0])
		os.environ[sp[0]] = sp[1]
            self.startOwnServer = True

        def stop(self):
	    logger.info("stopping dbus...")
            os.kill(int(os.environ["DBUS_SESSION_BUS_PID"]), signal.SIGTERM)
            for k in self.environ:
                if self.environ[k] is None:
		    del(os.environ[k])
 		else:
                    os.environ[k] = self.environ[k]
