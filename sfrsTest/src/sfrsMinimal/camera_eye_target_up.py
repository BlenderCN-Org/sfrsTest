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
# Created on                          06-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import bpy
import math

def old():
    m = bpy.context.scene.objects['Camera'].matrix_world
    print(m)
    k = m.copy()
    k.transpose()
    print ("pos")
    print ( [ round(co,4) for co in k[3] ])
    print ("dir")
    print ( [ round(co,4) for co in k[2] ])
    print ("up")
    print ( [ round(co,4) for co in k[1] ])
    print ("to")
    print ( [ round(co,4) for co in k[3] - k[2] ])


def getCameraPos():
    m = bpy.context.scene.objects['Camera'].matrix_world
    k = m.copy()
    k.transpose()
    eye = k[3]
    dir = k[2]
    up  = k[1]
    target = eye - dir
    return (eye , target , up)

def getFOV():
    C = bpy.context
    r = C.scene.objects['Camera'].data.angle
    return  math.degrees(r)



import bpy
import math
def getDepthOfField():
    C = bpy.context
    cam = C.scene.objects['EmptyCamera'].matrix_world.copy()
    foc = C.scene.objects['EmptyActor'].matrix_world.copy()
    cam.transpose()
    foc.transpose()
    cam_pos = cam[3]
    cam_dir = cam[2]
    foc_pos = foc[3]
    cam_foc = foc_pos - cam_pos
    dist = cam_foc.dot(cam_dir)
    perpendicular_distance = round(dist,5)
    direct_distance = cam_foc.length
    return (perpendicular_distance, direct_distance)
    


if __name__ == '__main__':
    getDepthOfField()