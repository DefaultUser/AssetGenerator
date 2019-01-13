# Asset Generator
# Copyright (C) <2015-2019>  <Sebastian Schmidt>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import re
import configparser
from contextlib import contextmanager
import functools
import numpy as np
from math import cos, sin


brushdef = '// brush\n{{\nbrushDef\n{{\n{data}}}\n}}\n'


@contextmanager
def worldspawn(f):
    f.write('//entity 0\n{\n"classname" "worldspawn"\n')
    yield
    f.write('\n}')


@contextmanager
def group(f, name):
    f.write('{\n"classname" "func_group"\n"targetname" "%s"\n' % name)
    yield
    f.write('\n}')


def point_to_str(point):
    return '( {} {} {} )'.format(*point)


def memoize(f):
    f.cache = {}

    @functools.wraps(f)
    def inner(*args, **kwargs):
        key = "(" + ", ".join([str(arg) for arg in args]) + ")"
        key = key + "|" + str(kwargs)
        if not key in f.cache:
            f.cache[key] = f(*args, **kwargs)
        return f.cache[key]
    return inner


@memoize
def xon_dir():
    """
    Get the base path of the Xonotic folder
    """
    conffile = os.path.join(os.path.dirname(__file__), "config.conf")
    cparser = configparser.ConfigParser()
    cparser.read(conffile)
    if not cparser.has_section("path"):
        cparser.add_section("path")
    if not cparser.has_option("path", "xondir"):
        xondir = input("Please specify the Xonotic base directory:\n")
        cparser.set("path", "xondir", xondir)
        with open(conffile, "w") as cf:
            cparser.write(cf)
    return cparser.get("path", "xondir")


@memoize
def is_git_build():
    if os.path.isdir(os.path.join(xon_dir(), "data", "xonotic-maps.pk3dir")):
        return True
    return False


@memoize
def find_maps_pk3():
    """
    Find the pk3 containing the map data
    """
    # TODO: support other games
    pat = re.compile(r"^xonotic-[\d\w]+-maps.pk3")
    datadir = os.path.join(xon_dir(), "data")
    for file in os.listdir(datadir):
        if pat.search(file):
            return os.path.join(datadir, file)


def find_maps_pk3dir():
    return os.path.join(xon_dir(), "data", "xonotic-maps.pk3dir")


@memoize
def find_mapping_support():
    """
    Find the pk3 with mapping support
    """
    # TODO: support other games
    pat = re.compile(r"^xonotic-\d+-maps-mapping.pk3")
    userdir = os.path.expanduser("~")
    if sys.platform == "win32" or sys.platform == "cygwin":
        configpath = os.path.join(userdir, "Saved Games", "xonotic", "data")
    elif sys.platform == "darwin":
        configpath = os.path.join(userdir, "Library", "Application Support",
                                  "xonotic", "data")
    else:
        configpath = os.path.join(userdir, ".xonotic", "data")
    for file in os.listdir(configpath):
        if pat.search(file):
            return os.path.join(configpath, file)

def RotationMatrixX(theta):
    """
    Rotation Matrix around X axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.array([[1,  0, 0],
                     [0,  c, s],
                     [0, -s, c]])

def RotationMatrixY(theta):
    """
    Rotation Matrix around Y axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.array([[ c, 0, s],
                     [ 0, 1, 0],
                     [-s, 0, c]])

def RotationMatrixZ(theta):
    """
    Rotation Matrix around Z axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.array([[ c, s, 0],
                     [-s, c, 0],
                     [ 0, 0, 1]])
