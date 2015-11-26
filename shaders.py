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

import re
import zipfile
import io
from PIL import Image
import helper


def get_texture_size(shadername):
    shader = find_shader(shadername)
    texpath = shader.texture_path
    # TODO: support custom textures
    return get_texture_size_mapping_support(texpath)


@helper.memoize
def get_texture_size_mapping_support(path):
    with zipfile.ZipFile(helper.find_mapping_support(), "r") as zf:
        # if no suffix is specified, use jpg
        if not "." in path.split("/")[-1]:
            path = path + ".jpg"
        # mapping support has jpg images, but tga images are defined
        # in the official shaders in Xonotic
        if path not in zf.namelist():
            path = path.replace(".tga", ".jpg")
        src = io.BytesIO(zf.read(path))
        img = Image.open(src)
        return img.size


def find_shader(name):
    filename = name.split("/")[0] + ".shader"
    shaders = parse_shader_file(filename)
    for shader in shaders:
        if shader.name == name:
            return shader


class Shader(object):
    def __init__(self, name, scanner):
        super().__init__()
        self.name = name
        self.parse_shader(scanner)

    def parse_shader(self, scanner):
        self.content = []
        match = scanner.match()
        while match.lastgroup in ['WS', 'COMMENT']:
            match = scanner.match()
        if not match.lastgroup == 'OPEN':
            raise ValueError("Shader definition does not start with an '{'")
        match = scanner.match()
        while match:
            if match.lastgroup in ['WS', 'COMMENT']:
                match = scanner.match()
                continue
            if match.lastgroup == 'CLOSE':
                match = scanner.match()
                break
            if match.lastgroup == 'OPEN':
                s = Stage(scanner)
                self.content.append(s)
            else:
                self.content.append(match.group())
            match = scanner.match()

    @property
    def texture_path(self):
        index = self.content.index("qer_editorimage")
        return self.content[index+1]


class Stage(object):
    def __init__(self, scanner):
        self.parse_stage(scanner)

    def parse_stage(self, scanner):
        self.content = []
        match = scanner.match()
        while match:
            if match.lastgroup in ['WS', 'COMMENT']:
                match = scanner.match()
                continue
            if match.lastgroup == 'CLOSE':
                match = scanner.match()
                break
            if match.lastgroup == 'OPEN':
                s = Stage(scanner)
                self.content.append(s)
            else:
                self.content.append(match.group())
            match = scanner.match()


@helper.memoize
def parse_shader_file(filename):
    """
    Mini shader parser, only does minimal amount of parsing.
    """
    tokens = re.compile(r'''
        (?P<WS>       \s            ) |
        (?P<COMMENT>  //[^\n]*\n    ) |
        (?P<OPEN>     \{            ) |
        (?P<CLOSE>    \}            ) |
        (?P<NUMBER>   -?\d*\.?\d+   ) |
        (?P<VECTOR>   \(\s*(-?\d*\.?\d+)\s+(-?\d*\.?\d+)\s+(-?\d*\.?\d+)\s*\) ) |
        (?P<QUOTED>   (?P<q>"|')[^\r\n]*[^\\](?P=q) ) |
        (?P<STRING>   [^\s]+        )
        ''', re.VERBOSE | re.MULTILINE)

    # TODO: support custom shader files and git builds (.pk3dir)
    with zipfile.ZipFile(helper.find_maps_pk3(), "r") as zf:
        data = zf.read("scripts/" + filename).decode()
    scanner = tokens.scanner(data)
    shaders = []
    match = scanner.match()
    while match:
        if match.lastgroup in ['WS', 'COMMENT']:
            match = scanner.match()
            continue
        if match.lastgroup == 'STRING':
            name = "/".join(match.group().split("/")[1:])
            s = Shader(name, scanner)
            shaders.append(s)
        else:
            print("The given shader file seems to contain errors")
        match = scanner.match()
    return shaders
