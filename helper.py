# Asset Generator
# Copyright (C) <2015>  <Sebastian Schmidt>

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

from contextlib import contextmanager


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
