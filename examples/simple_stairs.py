# Asset Generator
# Copyright (C) <2018>  <Sebastian Schmidt>

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
import primitives
import modifiers
import assets


if __name__ == "__main__":
    # create a single step
    step = primitives.Cuboid([0, 0, 8], [32, 128, 16], "trak6x/base-base1b")
    # use the array modifier to repeat the step
    steps = modifiers.Array(step, 16, [1, 0, 1.5], relative=True)
    # create a support beam by cutting a cuboid twice
    temp = primitives.Cuboid([248, 0, 176], [496, 16, 368], "trak6x/base-base1c")
    support_beam = temp.cutted(baseclasses.Face([8, 0, 8], [8, 32, 8],
                                                [40, 0, 32], "trak6x/base-base1c"),
                               baseclasses.Face([496, 0, 352], [496, 32, 352],
                                                [24, 0, 0], "trak6x/base-base1c"))
    # use the ObjectWriter to save the objects into a .map file
    # also group them into the func_group "Stairs"
    writer = assets.ObjectWriter([steps, support_beam], group="Stairs")
    with open("simple_stairs.map", "w") as f:
        writer.write(f)

