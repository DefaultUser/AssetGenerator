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

import baseclasses
import helper


class ObjectWriter(baseclasses.BaseAsset):
    def __init__(self, objs, group="Group"):
        super().__init__()
        self.objs = objs
        self.group = group

    def write(self, f):
        groupables = [obj for obj in self.objs if obj.isGroupable]
        nongroupables = [obj for obj in self.objs if not obj.isGroupable]
        if groupables:
            with helper.group(f, self.group):
                for obj in groupables:
                    f.write(str(obj))
        if nongroupables:
            with helper.worldspawn(f):
                for obj in nongroupables:
                    f.write(str(obj))
