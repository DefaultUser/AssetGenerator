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

from collections import defaultdict
from helper import point_to_str
from baseclasses import BaseObject


class Cuboid(BaseObject):
    isGroupable = True

    def __init__(self, center, size, texture=None):
        """
        \brief Generate a cuboid
        \param center center of the cuboid
        \param size size of the cuboid
        \param texture texture of the cuboid as string (applied to all faces)
        or as a dictionary with 'top','front' etc for individual faces
        """
        super().__init__(center, size)
        if not texture:
            texture = "common/caulk"
        if isinstance(texture, str):
            self.texture = defaultdict(lambda: texture)
        else:
            self.texture = defaultdict(lambda: "common/caulk", texture)

    def data_as_string(self):
        # TODO: rotation
        data = '// brush\n{\nbrushDef\n{\n'
        # plane 0 - top face
        p0 = (self.center[0] + self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p1 = (self.center[0] + self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p2 = (self.center[0] - self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] + self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(
            P0=point_to_str(p0), P1=point_to_str(p1), P2=point_to_str(p2),
            tex=self.texture["top"])

        # plane 1 - left face
        p0 = (self.center[0] + self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p1 = (self.center[0] - self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p2 = (self.center[0] + self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] - self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(P0=point_to_str(p0),
                                                                              P1=point_to_str(p1),
                                                                              P2=point_to_str(p2),
                                                                              tex=self.texture["left"])

        # plane 2 - back face
        p0 = (self.center[0] + self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p1 = (self.center[0] + self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p2 = (self.center[0] + self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] + self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(
            P0=point_to_str(p0), P1=point_to_str(p1), P2=point_to_str(p2),
            tex=self.texture["back"])

        # plane 3 - bottom face
        p0 = (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p1 = (self.center[0] + self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p2 = (self.center[0] - self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] - self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(
            P0=point_to_str(p0), P1=point_to_str(p1), P2=point_to_str(p2),
            tex=self.texture["bottom"])

        # plane 4 - right face
        p0 = (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p1 = (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] + self.size[2]/2)
        p2 = (self.center[0] + self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] - self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(
            P0=point_to_str(p0), P1=point_to_str(p1), P2=point_to_str(p2),
            tex=self.texture["right"])

        # plane 5 - front face
        p0 = (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p1 = (self.center[0] - self.size[0]/2, self.center[1] + self.size[1]/2,
              self.center[2] - self.size[2]/2)
        p2 = (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2,
              self.center[2] + self.size[2]/2)
        data += '{P0} {P1} {P2} ( ( 1 0 0 ) ( 0 1 0 ) ) {tex} 0 0 0\n'.format(
            P0=point_to_str(p0), P1=point_to_str(p1), P2=point_to_str(p2),
            tex=self.texture["front"])

        data += '}\n}\n'
        return data
