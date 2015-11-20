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


class ArrayModifier(object):
    def __init__(self, obj, count, offset, relative=False):
        """
        \brief Copy an object multiple times and place them with
        a certain offset
        \param obj Object that should be copied
        \param count Number of copies
        \param offset Offset between the copies
        \param relative use relaitve or absolute offset
        """
        self.obj = obj
        self.count = count
        self.offset = np.array(offset, dtype=np.float)
        self.relative = relative

    @property
    def isGroupable(self):
        return self.obj.isGroupable

    @property
    def center(self):
        return (self[0].center + self[self.count-1].center)/2

    def move(self, offset):
        self.obj.move(offset)

    @property
    def size(self):
        return self[self.count-1].center - self[0].center + self.obj.size

    def __len__(self):
        return self.count

    def __iter__(self):
        i = 0
        while i < self.count:
            yield self[i]
            i += 1

    def __getitem__(self, key):
        if type(key) != int:
            raise IndexError("Only integers are supported")
        obj = copy.deepcopy(self.obj)
        if self.relative:
            offset = self.offset*obj.size
        else:
            offset = self.offset
        obj.move((key % self.count)*offset)
        return obj

    def __str__(self):
        data = ""
        for obj in self:
            data += str(obj)
        return data
