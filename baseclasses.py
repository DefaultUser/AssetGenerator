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
import helper


class BaseAsset(object):
    def write(self, f):
        raise NotImplementedError("This is an abstract class")

    def save(self, path):
        """
        \brief Save the asset under a given name
        \param path filename (may be relative)
        """
        with open(path, "w") as f:
            self.write(f)


class BaseObject(object):
    isGroupable = False

    def __init__(self, center, size):
        super().__init__()
        self.center = center
        self.size = size

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = np.array(value, dtype=np.float)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = np.array(value, dtype=np.float)

    def __str__(self):
        raise NotImplementedError("This is an abstract class")


class Face(object):
    def __init__(self, v0, v1, v2, texture="common/caulk", angle=0,
                 x_off=0, y_off=0, x_scale=1, y_scale=1):
        super().__init__()
        self.verts = [v0, v1, v2]
        self.texture = texture
        self.angle = angle
        self.offset = np.array([x_off, y_off], dtype=np.float)
        self.scale = np.array([x_scale, y_scale], dtype=np.float)

    def __str__(self):
        base = ('{P0} {P1} {P2} ( ( {rs[0][0]} {rs[0][1]} {off[0]} )'
                ' ( {rs[1][0]} {rs[1][1]} {off[1]} ) ) {tex} 0 0 0\n')
        # TODO: get texture size from texture
        texsize = np.array([64, 64], dtype=np.float)
        cos_angle = np.cos(np.deg2rad(self.angle))
        sin_angle = np.sin(np.deg2rad(self.angle))
        rot = np.array([[cos_angle, sin_angle], [-sin_angle, cos_angle]])
        rotscale = rot/(texsize*self.scale)
        return base.format(P0=helper.point_to_str(self.verts[0]),
                           P1=helper.point_to_str(self.verts[1]),
                           P2=helper.point_to_str(self.verts[2]),
                           rs=rotscale, off=self.offset/texsize,
                           tex=self.texture)


class Brush(BaseObject):
    isGroupable = True

    @property
    def faces(self):
        raise NotImplementedError("This is an abstract class")

    def __str__(self):
        data = ''
        for face in self.faces:
            data += str(face)
        return helper.brushdef.format(data=data)
