#-*- coding: utf-8 -*-
""" process templates with paramenters.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2015-12-02
    Licence: GPL-2+
"""

import os
import shutil

BASEPATH = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.join(BASEPATH, "templates/")

def setupConfigDirs(dirname, fullPrimaryEmail, primaryEmail, name, uid, password):
    """copy files in basedir to dirname and replace every {name} etc. with the content of the parameter."""

    d = {"fullPrimaryEmail": fullPrimaryEmail,
	 "primaryEmail": primaryEmail,
	 "name": name,
	 "uid": uid,
	 "password": password}

    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != 17:
	   raise
    for path, _, files in os.walk(basedir):
	relpath = os.path.relpath(path,basedir)
	try:
		os.mkdir(os.path.join(dirname, relpath))
	except OSError as e:
             if e.errno != 17:
                 raise
        for fname in files:
            if os.path.splitext(fname)[1] in (".kwl",):
		shutil.copy(os.path.join(path,fname), os.path.join(dirname, relpath, fname))
                continue
            with open(os.path.join(path,fname),"r") as f:
		with open(os.path.join(dirname, relpath, fname),"w") as t:
			content = f.read().format(**d)
			t.write(content)

if __name__ == "__main__":
	setupConfigDirs(".", "John Doe <doe@example.org>", "doe@example.org", "John Doe", "doe", "Welcome2KolabSystems")
