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
import baseclasses


class Cuboid(baseclasses.BasePrimitive, baseclasses.Brush):
    def __init__(self, center, size, texture="common/caulk"):
        """
        \brief Generate a cuboid
        \param center center of the cuboid
        \param size size of the cuboid
        \param texture texture of the cuboid as string (applied to all faces)
        or as a dictionary with 'top','front' etc for individual faces
        """
        super().__init__(center, size)
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
        return [baseclasses.Face(verts[0], verts[1], verts[3],
                                 self.texture["front"]),
                baseclasses.Face(verts[5], verts[4], verts[6],
                                 self.texture["back"]),
                baseclasses.Face(verts[4], verts[0], verts[7],
                                 self.texture["right"]),
                baseclasses.Face(verts[1], verts[5], verts[2],
                                 self.texture["left"]),
                baseclasses.Face(verts[4], verts[5], verts[0],
                                 self.texture["bottom"]),
                baseclasses.Face(verts[3], verts[2], verts[7],
                                 self.texture["top"])]


class CylinderBrush(baseclasses.BasePrimitive, baseclasses.Brush):
    def __init__(self, center, radius, height, radius2=0, numSides=16,
                 texture="common/caulk"):
        """
        \brief Generate a Cylinder with numSides sides
        \param center center of the cylinder
        \param radius radius of the base area
        \param height height of the cylinder
        \param radius2 if != 0 generate a cylinder with eliptical base area
        \param numSides number of sides of the cylinder
        \param texture texture of the cylinder as string (applied to all faces)
        or as a dictionary('top', 'bottom' and 'sides') for individual faces
        """
        size = np.array([2*radius, 2*radius2, height], dtype=np.float)
        super().__init__(center, size)
        self.numSides = numSides
        if isinstance(texture, str):
            self.texture = defaultdict(lambda: texture)
        else:
            self.texture = defaultdict(lambda: "common/caulk", texture)

    @property
    def size(self):
        return np.array([2*self.radius, 2*self.radius, self.height],
                        dtype=np.float)

    @size.setter
    def size(self, value):
        self.radius = value[0]/2
        self.radius2 = value[1]/2
        self.height = value[2]

    @property
    def faces(self):
        faces = []
        rad2 = self.radius2 if self.radius2 else self.radius
        # sides
        angle = 2*np.pi/self.numSides
        for i in range(self.numSides):
            v0 = self.center + np.array([self.radius*np.cos((i+1)*angle),
                                         rad2*np.sin((i+1)*angle),
                                         -self.height/2], dtype=np.float)
            v1 = self.center + np.array([self.radius*np.cos((i)*angle),
                                         rad2*np.sin((i)*angle),
                                         -self.height/2], dtype=np.float)
            v2 = self.center + np.array([self.radius*np.cos((i+1)*angle),
                                         rad2*np.sin((i+1)*angle),
                                         +self.height/2], dtype=np.float)
            faces.append(baseclasses.Face(v0, v1, v2, self.texture["sides"]))
        # top
        v0 = self.center + np.array([self.radius, -self.radius,
                                     self.height/2], dtype=np.float)
        v1 = self.center + np.array([-self.radius, -self.radius,
                                     self.height/2], dtype=np.float)
        v2 = self.center + np.array([self.radius, self.radius,
                                     self.height/2], dtype=np.float)
        faces.append(baseclasses.Face(v0, v1, v2, self.texture["top"]))
        # bottom
        v0 = self.center + np.array([self.radius, self.radius,
                                     -self.height/2], dtype=np.float)
        v1 = self.center + np.array([-self.radius, self.radius,
                                     -self.height/2], dtype=np.float)
        v2 = self.center + np.array([self.radius, -self.radius,
                                     -self.height/2], dtype=np.float)
        faces.append(baseclasses.Face(v0, v1, v2, self.texture["bottom"]))
        return faces


class EllipsoidBrush(baseclasses.BasePrimitive, baseclasses.Brush):
    def __init__(self, center, size, numSegments=16, numRings=16,
                 texture="common/caulk"):
        super().__init__(center, size)
        self.numSegments = numSegments
        self.numRings = numRings
        self.texture = texture

    @property
    def faces(self):
        faces = []
        segmentAngle = 2*np.pi/self.numSegments
        ringAngle = np.pi/self.numRings

        for i_seg in range(self.numSegments):
            # faces of the lowest ring have to be computed differently
            mu_i = -np.pi/2
            nu_i = i_seg*segmentAngle
            mu_ip1 = ringAngle - np.pi/2
            nu_ip1 = (i_seg+1)*segmentAngle

            v0_normalized = np.array([np.cos(mu_ip1)*np.cos(nu_ip1),
                                      np.cos(mu_ip1)*np.sin(nu_ip1),
                                      np.sin(mu_ip1)], dtype=np.float)
            v1_normalized = np.array([np.cos(mu_i)*np.cos(nu_ip1),
                                      np.cos(mu_i)*np.sin(nu_ip1),
                                      np.sin(mu_i)], dtype=np.float)
            v2_normalized = np.array([np.cos(mu_ip1)*np.cos(nu_i),
                                      np.cos(mu_ip1)*np.sin(nu_i),
                                      np.sin(mu_ip1)], dtype=np.float)

            v0 = v0_normalized*self.size/2 + self.center
            v1 = v1_normalized*self.size/2 + self.center
            v2 = v2_normalized*self.size/2 + self.center
            faces.append(baseclasses.Face(v0, v1, v2, self.texture))

            # rest of the rings
            for i_ring in range(1, self.numRings):
                mu_i = i_ring*ringAngle - np.pi/2
                nu_i = i_seg*segmentAngle
                mu_ip1 = (i_ring+1)*ringAngle - np.pi/2
                nu_ip1 = (i_seg+1)*segmentAngle

                v0_normalized = np.array([np.cos(mu_i)*np.cos(nu_ip1),
                                          np.cos(mu_i)*np.sin(nu_ip1),
                                          np.sin(mu_i)], dtype=np.float)
                v1_normalized = np.array([np.cos(mu_i)*np.cos(nu_i),
                                          np.cos(mu_i)*np.sin(nu_i),
                                          np.sin(mu_i)], dtype=np.float)
                v2_normalized = np.array([np.cos(mu_ip1)*np.cos(nu_ip1),
                                          np.cos(mu_ip1)*np.sin(nu_ip1),
                                          np.sin(mu_ip1)], dtype=np.float)

                v0 = v0_normalized*self.size/2 + self.center
                v1 = v1_normalized*self.size/2 + self.center
                v2 = v2_normalized*self.size/2 + self.center
                faces.append(baseclasses.Face(v0, v1, v2, self.texture))

        return faces
