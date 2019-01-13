# Asset Generator
# Copyright (C) <2019>  <Sebastian Schmidt>

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

import sys
import os

# put parent directory into PYTHONPATH, remove this when this library has a proper setup.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import baseclasses
import assets
import math
import numpy as np
import helper


if __name__ == "__main__":
    # create a single step, inner radius 64, outer radius 256
    r1 = 64.0
    r2 = 256.0
    stepheight = 24.0
    theta = math.radians(15)
    rot_matrix = helper.RotationMatrixZ(theta)
    v0 = np.array([r1, 0, 0], dtype=np.float64)
    v1 = np.array([r2, 0, 0], dtype=np.float64)
    v2 = v0 @ rot_matrix
    v3 = v1 @ rot_matrix
    v4 = v0 + [0, 0, stepheight]
    v5 = v1 + [0, 0, stepheight]
    f0 = baseclasses.Face(v0, v1, v2, "trak6x/base-base1c")
    f1 = f0.flipped()
    f1.move([0, 0, stepheight])
    f2 = baseclasses.Face(v0, v2, v4)
    f3 = baseclasses.Face(v0, v4, v1, "trak6x/base-base1c")
    f4 = f3.flipped().rotated_point([0, 0, 0], rot_matrix)
    f5 = baseclasses.Face(v1, v5, v3)
    step = baseclasses.Brush([f0, f1, f2, f3, f4, f5])
    # inner and outer ramps, 8 units wide
    ramp_width = 8.0
    v6 = np.array([r1-ramp_width, 0, -stepheight])
    v7 = v6 @ rot_matrix + [0, 0, stepheight]
    v8 = np.array([r1-ramp_width, 0, stepheight])
    v9 = v8 @ rot_matrix + [0, 0, stepheight]
    v10 = v0 - [0, 0, stepheight]
    v11 = v2 + [0, 0, 2*stepheight]
    v12 = v4 - [ramp_width, 0, 0]
    f6 = baseclasses.Face(v10, v4, v2, "trak6x/base-base1c")
    f7 = baseclasses.Face(v10, v6, v4, "trak6x/base-base1c")
    f8 = baseclasses.Face(v10, v2, v6, "trak6x/base-base1c")
    f9 = baseclasses.Face(v4, v12, v11, "trak6x/base-base1c")
    f10 = baseclasses.Face(v6, v2, v12)
    inner_ramp1 = baseclasses.Brush([f6, f7, f8, f9, f10])
    v13 = v12 @ rot_matrix + [0, 0, stepheight]
    f11 = baseclasses.Face(v6, v7, v12, "trak6x/base-base1c")
    f12 = baseclasses.Face(v6, v2, v7, "trak6x/base-base1c")
    f13 = baseclasses.Face(v7, v2, v13, "trak6x/base-base1c")
    f14 = baseclasses.Face(v12, v13, v11, "trak6x/base-base1c")
    f15 = f10.flipped()
    inner_ramp2 = baseclasses.Brush([f11, f12, f13, f14, f15])
    v14 = np.array([r2+ramp_width, 0, -stepheight])
    v15 = v1 - [0, 0, stepheight]
    v16 = np.array([r2+ramp_width, 0, stepheight])
    v17 = v15 @ rot_matrix + [0, 0, stepheight]
    v18 = v14 @ rot_matrix + [0, 0, stepheight]
    v19 = v17 + [0, 0, 2*stepheight]
    v20 = v18 + [0, 0, 2*stepheight]
    f16 = baseclasses.Face(v15, v17, v5, "trak6x/base-base1c")
    f17 = baseclasses.Face(v15, v18, v17, "trak6x/base-base1c")
    f18 = baseclasses.Face(v17, v18, v19, "trak6x/base-base1c")
    f19 = baseclasses.Face(v5, v19, v20, "trak6x/base-base1c")
    f20 = baseclasses.Face(v15, v5, v18)
    outer_ramp1 = baseclasses.Brush([f16, f17, f18, f19, f20])
    f21 = baseclasses.Face(v14, v15, v16, "trak6x/base-base1c")
    f22 = baseclasses.Face(v15, v14, v18, "trak6x/base-base1c")
    f23 = baseclasses.Face(v16, v5, v20, "trak6x/base-base1c")
    f24 = baseclasses.Face(v14, v16, v18, "trak6x/base-base1c")
    f25 = f20.flipped()
    outer_ramp2 = baseclasses.Brush([f21, f22, f23, f24, f25])
    # copy, rotate and move the step
    steps = [step]
    inner = [inner_ramp1, inner_ramp2]
    outer = [outer_ramp1, outer_ramp2]
    for i in range(11):
        # TODO: rotation support for array modifier
        temp = steps[-1].copy_brush()
        temp.rotate_point([0, 0, 0], rot_matrix)
        temp.move([0, 0, stepheight])
        steps.append(temp)
        # inner ramps
        temp = inner[-2].copy_brush()
        temp.rotate_point([0, 0, 0], rot_matrix)
        temp.move([0, 0, stepheight])
        inner.append(temp)
        temp = inner[-2].copy_brush()
        temp.rotate_point([0, 0, 0], rot_matrix)
        temp.move([0, 0, stepheight])
        inner.append(temp)
        # outer ramps
        temp = outer[-2].copy_brush()
        temp.rotate_point([0, 0, 0], rot_matrix)
        temp.move([0, 0, stepheight])
        outer.append(temp)
        temp = outer[-2].copy_brush()
        temp.rotate_point([0, 0, 0], rot_matrix)
        temp.move([0, 0, stepheight])
        outer.append(temp)
    # use the ObjectWriter to save the objects into a .map file
    # also group them into the func_group "Stairs"
    writer = assets.ObjectWriter(steps + inner + outer, group="Stairs")
    with open("spiral_stairs.map", "w") as f:
        writer.write(f)
