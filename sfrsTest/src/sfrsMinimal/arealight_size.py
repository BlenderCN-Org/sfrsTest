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
# Created on                          11-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import bpy
import math
import mathutils




def get_area_light():
    C= bpy.context
    light = C.scene.objects['Lamp']
    if (light.type == 'LAMP') & (light.data.type == 'AREA'):
        print("Lamp type found")
    else:
        return
    
    obj_matrix = light.matrix_world.copy()
    
    #--------------------------------------------------------- print(obj_matrix)
    #---------------------------------------------------- print(light.data.size)
    #-------------------------------------------------- print(light.data.size_y)
    #--------------------------------------------------- print(light.data.shape)
    
    size_x = light.data.size  
    size_y = light.data.size_y  
    pts = [ (-size_x/2.0 , size_y/2.0), (size_x/2.0 , size_y/2.0), (size_x/2.0 , -size_y/2.0), (-size_x/2.0 , -size_y/2.0)]
    
    trArea = []
    for vert in pts:
        trArea.append( [ "%+0.4f" %point for point in (obj_matrix * mathutils.Vector([vert[0], vert[1], 0, 1])).to_tuple() ])
    print (trArea)
    
    trFaces = [[0,1,2], [2,3,0]]
    return(trArea, trFaces)
    


if __name__ == '__main__':
    get_area_light()