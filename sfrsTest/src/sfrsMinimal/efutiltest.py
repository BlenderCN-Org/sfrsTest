# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender Version                     2.68
# Exporter Version                    0.0.1
# Created on                          14-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import os
import bpy


# Framework libs
from extensions_framework import util as efutil





def getServices():
    cube = bpy.context.scene.objects['Cube']
    path = cube.material_slots[0].material.texture_slots[0].texture.image.filepath
    xfac = efutil.filesystem_path(path)
    print("path now>> %s" % xfac)
    abs = os.path.abspath(xfac)
    print("path abs>> %s" % abs)
    rel = efutil.path_relative_to_export(path)
    print("path rel>> %s" % rel)


if __name__ == '__main__':
    getServices()
