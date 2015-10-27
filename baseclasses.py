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
        self.center = np.array(center, dtype=np.float)
        self.size = np.array(size, dtype=np.float)

    def _str__(self):
        raise NotImplementedError("This is an abstract class")


class Brush(BaseObject):
    isGroupable = True

    @property
    def faces(self):
        raise NotImplementedError("This is an abstract class")

    def __str__(self):
        data = ''
        for face in self.faces:
            data += helper.faceplane.format(P0=helper.point_to_str(face[0]),
                                            P1=helper.point_to_str(face[1]),
                                            P2=helper.point_to_str(face[2]),
                                            tex=face[3])
        return helper.brushdef.format(data=data)
