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
# Created on                          29-Jul-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import bpy
import math
import mathutils



def caller():
    context= bpy.context
    scene = context.scene
    objects = scene.objects
    
    
    
    for each in objects:
        if each.type in ['MESH']:
            print ("@Mesh: " + each.name)
            mesh = each.data
            obj_matrix = each.matrix_world
            vertices = [ v   for v in mesh.vertices ]
            for cord in vertices:
                x = cord.co.x
                y = cord.co.y
                z = cord.co.z
                matrix = obj_matrix * cord.co
                print ("      @vertices: %+0.4f  %+0.4f  %+0.4f " %(x,y,z))
                print (matrix)
    


def caller_dupli():
    context= bpy.context
    scene = context.scene
    objects = scene.objects
    
    print ("\n"*8)
    
    for obj_main in objects:
        if obj_main.type in ['MESH']:
            if obj_main.parent and obj_main.parent.dupli_type in {'VERTS', 'FACES'}:
                print(obj_main.name, 'is a dupli child - ignoring')
                continue
    
            obs = []
            if obj_main.dupli_type != 'NONE':
                # XXX
                print('creating dupli_list on', obj_main.name)
                obj_main.dupli_list_create(scene)
    
                obs = [(dob.object, dob.matrix) for dob in obj_main.dupli_list]
    
                # XXX debug print
                print(obj_main.name, 'has', len(obs), 'dupli children')
            else:
                obs = [(obj_main, obj_main.matrix_world)]
                
            

            for ob, ob_mat in obs:
                #--------------------------------------------- print ("@  mat:")
                #------------------------------------------------ print (ob_mat)
                pos, rot, sca = ob_mat.decompose()
                #--------------------------------------------------- print (pos)
                reu = rot.to_euler('XYZ')
                x,y,z = (math.degrees(reu.x), math.degrees(reu.y), math.degrees(reu.z))
                #----------------------------------------------- print ((x,y,z))
                #--------------------------------------------------- print (sca)
                
                
            #===================================================================
            # to file
            #===================================================================
            
            theOriginalObjectName = "Monkey"
            Instance = 0
            shaderForInstance = "Green.shader"
            
            for ob, ob_mat in obs:
                pos, rot, sca = ob_mat.decompose()
                reu = rot.to_euler('XYZ')
                x,y,z = (math.degrees(reu.x), math.degrees(reu.y), math.degrees(reu.z))
                
                print ("instance {")
                print ("        name " + theOriginalObjectName + "_" + str(Instance))
                print ("        geometry " + theOriginalObjectName)
                print ("        transform {")
                print ("                translate  %+0.4f   %+0.4f   %+0.4f " %(pos.x, pos.y , pos.z))
                print ("                rotatex    %+0.4f  " %(x))
                print ("                rotatey    %+0.4f  " %(y))
                print ("                rotatez    %+0.4f  " %(z))
                print ("                scaleu     %+0.4f  " %(1.0))
                print ("                  }")
                print ("        shader  " + shaderForInstance)
                print ("         }")
                print ("         ")
                print ("         ")
                Instance += 1
            if obj_main.dupli_type != 'NONE':
                obj_main.dupli_list_clear()


#===============================================================================
# instance {
#  name nameOfInstance
#  geometry theOriginalObjectName
#  transform {
#     rotatex -90
#     scaleu 1.0
#     translate -1.0 3.0 -1.0
#  }
#  shader shaderForInstance
#  modifier modForInstance
# }
# 
# 
# transform {
#      translate 1.0 4.6 0.3
#      scaleu 0.5
#   }
# 
# translate (translate x y z)
# rotatex
# rotatey
# rotatex
# scalex
# scaley
# scalez
# scaleu
#===============================================================================

if __name__ == '__main__':
    caller_dupli()