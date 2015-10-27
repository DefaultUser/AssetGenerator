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
import numpy as np
from helper import point_to_str
import baseclasses


class Cuboid(baseclasses.Brush):
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

    @property
    def verticies(self):
        """
        \brief Returns a list of all verticies, starting in the right bottom
        corner of the front face, going clockwise and then the back face
        """
        # TODO: rotation
        basecuboid = np.array([[-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5],
                               [-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5],
                               [0.5, -0.5, -0.5], [0.5, 0.5, -0.5],
                               [0.5, 0.5, 0.5], [0.5, -0.5, 0.5]])
        return self.center + self.size*basecuboid

    @property
    def faces(self):
        """
        \brief Return the faces described by 3 verticies and the texture
        order: front, back, right, left, bottom, top
        """
        verts = self.verticies
        return [[verts[0], verts[1], verts[3], self.texture["front"]],
                [verts[5], verts[4], verts[6], self.texture["back"]],
                [verts[4], verts[0], verts[7], self.texture["right"]],
                [verts[1], verts[5], verts[2], self.texture["left"]],
                [verts[4], verts[5], verts[0], self.texture["bottom"]],
                [verts[3], verts[2], verts[7], self.texture["top"]]]
