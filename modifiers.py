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


class Array(object):
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
        self.offset = offset
        self.relative = relative

    @property
    def isGroupable(self):
        return self.obj.isGroupable

    @property
    def center(self):
        return (self[0].center + self[self.count-1].center)/2

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = np.array(value, dtype=np.float)

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


class RandomScatter(object):
    def __init__(self, obj, count, max_offset, scale_variation=0):
        """
        \brief Copy an object multiple times and place them with
        a random offset and scale
        \param obj Object that should be copied
        \param count Number of copies
        \param max_offset Maximum offset of the scattered objects
        \param scale_variation Variation of the objects scale
        0 means no change in scale
        """
        self.obj = obj
        self.count = count
        self.max_offset = max_offset
        self.scale_variation = scale_variation

    @property
    def isGroupable(self):
        return self.obj.isGroupable

    @property
    def center(self):
        return self.obj.center

    @property
    def max_offset(self):
        return self._max_offset

    @max_offset.setter
    def max_offset(self, value):
        self._max_offset = np.array(value, dtype=np.float)

    def move(self, offset):
        self.obj.move(offset)

    @property
    def size(self):
        return self.max_offset + self.obj.size

    @property
    def scale_variation(self):
        return self._scale_variation

    @scale_variation.setter
    def scale_variation(self, value):
        self._scale_variation = np.array(value, dtype=np.float)

    def randomize_objects(self):
        """
        Do the actual randomizing
        """
        objs = []
        for i in range(self.count):
            obj = copy.deepcopy(self.obj)
            offsets = 2*(np.random.rand(3)-0.5)*self.max_offset
            obj.move(offsets)
            scales = 2*(np.random.rand()-0.5)*self.scale_variation + 1
            obj.scale(scales)
            objs.append(obj)
        return objs

    def __str__(self):
        data = ""
        for obj in self.randomize_objects():
            data += str(obj)
        return data
