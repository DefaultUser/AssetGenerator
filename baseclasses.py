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
import helper
import shaders


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


class BasePrimitive(object):
    """
    Abstract base class for all primitives (brushes and patches)
    """

    def __init__(self, center, size):
        self.center = center
        self.size = size

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = np.array(value, dtype=np.float)

    def move(self, offset):
        self.center += np.array(offset, dtype=np.float)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = np.array(value, dtype=np.float)

    def scale(self, factor):
        self.size *= factor


class Face(object):
    def __init__(self, v0, v1, v2, texture="common/caulk", angle=0,
                 x_off=0, y_off=0, x_scale=1, y_scale=1):
        super().__init__()
        self.verts = [np.array(v0, dtype=np.float),
                      np.array(v1, dtype=np.float),
                      np.array(v2, dtype=np.float)]
        self.texture = texture
        self.angle = angle
        self.offset = np.array([x_off, y_off], dtype=np.float)
        self.scale = np.array([x_scale, y_scale], dtype=np.float)

    def move(self, offset):
        """
        \brief move the face by a given offset (scalar or list of length 3)
        """
        for vert in self.verts:
            vert += np.array(offset, dtype=np.float)

    def __str__(self):
        base = ('{P0} {P1} {P2} ( ( {rs[0][0]} {rs[0][1]} {off[0]} )'
                ' ( {rs[1][0]} {rs[1][1]} {off[1]} ) ) {tex} 0 0 0\n')

        try:
            texsize = np.array(shaders.get_texture_size(self.texture),
                               dtype=np.float)
        except (KeyError, ValueError):
            print("WARNING: size of shader {} not found, "
                  "using a size of (64, 64)".format(self.texture))
            texsize = np.array([64, 64], dtype=np.float)

        cos_angle = np.cos(np.deg2rad(self.angle))
        sin_angle = np.sin(np.deg2rad(self.angle))
        rot = np.array([[cos_angle, sin_angle], [-sin_angle, cos_angle]])
        rotscale = rot/(texsize*self.scale)
        return base.format(P0=helper.point_to_str(self.verts[0]),
                           P1=helper.point_to_str(self.verts[1]),
                           P2=helper.point_to_str(self.verts[2]),
                           rs=rotscale, off=-self.offset/texsize,
                           tex=self.texture)


class Brush(object):
    isGroupable = True

    def __init__(self, faces):
        self.faces = faces

    @property
    def center(self):
        # TODO: implement this function
        raise NotImplementedError("Will come in the future")

    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, faces):
        if len(faces) < 4:
            raise AttributeError("Need at least 4 faces to form a brush")
        for face in faces:
            if not isinstance(face, Face):
                raise TypeError("List of 'Face' objects expected")
        self._faces = faces

    def move(self, offset):
        for face in self.faces:
            for vert in face.verts:
                vert += np.array(offset, dtype=np.float)

    def scale(self, factor):
        # TODO: implement this function
        raise NotImplementedError("Will come in the future")

    def cutted(self, *newfaces):
        """
        \brief create another brush by cutting this brush
        with the supplied faces
        """
        faces = copy.deepcopy(self.faces)
        for newface in newfaces:
            if type(newface) == Face:
                faces.append(newface)
            else:
                raise TypeError("Needs Face objects")
        return Brush(faces)

    def copy_brush(self):
        """
        \brief return an independent copy of the brush
        """
        faces = copy.deepcopy(self.faces)
        return Brush(faces)

    def __str__(self):
        data = ''
        for face in self.faces:
            data += str(face)
        return helper.brushdef.format(data=data)
