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

import numpy as np
import copy
import baseclasses
import helper


class ArrayModifier(baseclasses.BaseAsset):
    def __init__(self, obj, count, offset, relative=False,
                 group="ArrayModifier"):
        """
        \brief Copy an object multiple times and place them with
        a certain offset
        \param obj Object that should be copied
        \param count Number of copies
        \param offset Offset between the copies
        \param relative use relaitve or absolute offset
        """
        super().__init__()
        self.obj = obj
        self.count = count
        self.offset = np.array(offset, dtype=np.float)
        self.relative = relative
        self.group = group

    def write(self, f):
        if self.obj.isGroupable:
            context = helper.group
            args = [f, self.group]
        else:
            context = helper.worldspawn
            args = [f, ]

        # Don't modify the original
        obj = copy.deepcopy(self.obj)
        with context(*args):
            for i in range(self.count):
                if self.relative:
                    offset = self.offset*obj.size
                else:
                    offset = self.offset
                obj.center = self.obj.center + i*offset
                f.write(obj.data_as_string())
