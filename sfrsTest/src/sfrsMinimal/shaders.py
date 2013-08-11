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
# Created on                          10-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import os
import bpy
import math
import mathutils





def test_working():
    print("This will give the collection of materials in the scene.")
    print( bpy.data.materials )
    print("This will give material on a particular object 'CUBE'")
    print(bpy.context.scene.objects['Cube'].data.materials[:])
    print("This will give all the material slots on that object")
    print(bpy.context.scene.objects['Cube'].material_slots[:])
    print("This wil give the material assigned to a particular slot")
    print(bpy.context.scene.objects['Cube'].material_slots[0].material)
    


def tr_color_str(_color):
    colors = [ "%+0.4f" %channel for channel in _color ]
    return '  '.join(colors)



def texture_found(mat, mat_slot):
    if not mat.texture_slots:
        return False
    if not mat.texture_slots[mat_slot]:
        return False
    if not mat.texture_slots[mat_slot].texture:
        return False
    if not mat.texture_slots[mat_slot].texture_coords == 'UV':
        return False
    if not mat.texture_slots[mat_slot].texture.type == 'IMAGE':
        return False
    if not mat.texture_slots[mat_slot].texture.image :
        return False
    if not mat.texture_slots[mat_slot].texture.image.filepath:
        return False
    if mat.texture_slots[mat_slot].texture.image.packed_file:
        return False
    path = mat.texture_slots[mat_slot].texture.image.filepath
    #TODO: resolve relative path 
    if not os.path.exists(path):
        return False
    return True


def texture_path(mat, mat_slot):
    return mat.texture_slots[mat_slot].texture.image.filepath


def create_shader_block(mat):
    sfmat = mat.sunflow_material
    name = mat.name
    act_mat = [] 
    indent = 0
    space = "        "
    TYPE_meshlight = False
    
    act_mat.append("%s %s %s" %(space* indent , "shader", "{"))
    indent += 1
    act_mat.append("%s %s %s" %(space* indent , "name", name ))
    act_mat.append("%s %s %s" %(space* indent , "type", sfmat.type ))
    if sfmat.type == 'constant':        
        act_mat.append("%s %s %s" %(space* indent , "color  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str(sfmat.constantEmit * sfmat.diffuseColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
    elif sfmat.type == 'diffuse':        
        if not texture_found(mat , 0):                  # 0 means diffuse channel
            act_mat.append("%s %s %s" %(space* indent , "color  ", "{")) 
            indent += 1
            act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
            act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
            indent -= 1
        else:
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "texture ", texpath )) 
    elif sfmat.type == 'phong':        
        if not texture_found(mat , 0):                  # 0 means diffuse channel
            act_mat.append("%s %s %s" %(space* indent , "diff  ", "{")) 
            indent += 1
            act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
            act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
            indent -= 1
        else:
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "texture ", texpath )) 
        #spec channel
        act_mat.append("%s %s %s" %(space* indent , "spec  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.specularColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", sfmat.phongSpecHardness )) 
        indent -= 1
        
        act_mat.append("%s %s %s" %(space* indent , "samples", sfmat.phongSamples )) 
    elif sfmat.type == 'shiny':        
        if not texture_found(mat , 0):                  # 0 means diffuse channel
            act_mat.append("%s %s %s" %(space* indent , "diff  ", "{")) 
            indent += 1
            act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
            act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
            indent -= 1
        else:
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "texture ", texpath ))     
           
        if sfmat.shinyExponent :
            act_mat.append("%s %s %s" %(space* indent , "refl  ", "%+0.4f" %math.pow(10,4*sfmat.shinyReflection) ))     
        else:
            act_mat.append("%s %s %s" %(space* indent , "refl  ", "%+0.4f" %sfmat.shinyReflection ))     
        
   
    elif sfmat.type == 'glass':        

        act_mat.append("%s %s %s" %(space* indent , "eta  ", "%+0.4f" %sfmat.glassETA )) 

        act_mat.append("%s %s %s" %(space* indent , "color ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
   
        act_mat.append("%s %s %s" %(space* indent , "absorbtion.distance", "%+0.4f" %sfmat.glassAbsDistance )) 
        
        act_mat.append("%s %s %s" %(space* indent , "absorbtion.color", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.glassAbsColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
                
    elif sfmat.type == 'mirror':
        
        act_mat.append("%s %s %s" %(space* indent , "refl  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.mirrorReflection) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        
    elif sfmat.type == 'ward':        
        if not texture_found(mat , 0):                  # 0 means diffuse channel
            act_mat.append("%s %s %s" %(space* indent , "diff  ", "{")) 
            indent += 1
            act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
            act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
            indent -= 1
        else:
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "texture ", texpath )) 
        #spec channel
        act_mat.append("%s %s %s" %(space* indent , "spec  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.specularColor) ))        
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        
        act_mat.append("%s %s %s" %(space* indent , "rough ", "%+0.4f   %+0.4f" %(sfmat.wardRoughX  , sfmat.wardRoughY )  )) 
        act_mat.append("%s %s %s" %(space* indent , "samples", sfmat.wardSamples )) 
    
        
        
    elif sfmat.type == 'amb-occ':        
        if not texture_found(mat , 0):                  # 0 means diffuse channel
            act_mat.append("%s %s %s" %(space* indent , "bright  ", "{")) 
            indent += 1
            act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.ambientBright) )) 
            act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
            indent -= 1
        else:
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "texture ", texpath )) 
        #spec channel
        act_mat.append("%s %s %s" %(space* indent , "dark   ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.ambientDark) ))
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        
        act_mat.append("%s %s %s" %(space* indent , "samples", sfmat.ambientSamples  )) 
        act_mat.append("%s %s %s" %(space* indent , "dist  ", "%+0.4f" %(sfmat.ambientDistance)  )) 
        
    
        
    elif sfmat.type == 'uber':        
        #diffuse channel
        act_mat.append("%s %s %s" %(space* indent , "diff  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        #diffuse texture
        if  texture_found(mat , 0):                  # 0 means diffuse channel
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "diff.texture ", texpath )) 
            
        act_mat.append("%s %s %s" %(space* indent , "diff.blend", "%+0.4f" %(sfmat.uberDiffBlend )) )
    
        #spec channel
        act_mat.append("%s %s %s" %(space* indent , "spec  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.specularColor) ))        
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        
        #spec texture
        if  texture_found(mat , 1):                  # 1 means spec channel
            texpath = '"' + texture_path(mat , 0) + '"'
            act_mat.append("%s %s %s" %(space* indent , "spec.texture ", texpath )) 
            
        act_mat.append("%s %s %s" %(space* indent , "spec.blend", "%+0.4f" %(sfmat.uberSpecBlend )) ) 
    
    
        act_mat.append("%s %s %s" %(space* indent , "glossy ", "%+0.4f" %(sfmat.uberGlossy )  )) 
        act_mat.append("%s %s %s" %(space* indent , "samples", sfmat.uberSamples )) 
    
        
    act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
    indent -= 1
        
    # special types -- not directly found in sunflow usual;
    if sfmat.type == "janino" :
        act_mat = []
        path = '"'+sfmat.janinoPath+ '"'
        act_mat.append("%s %s %s" %(space* indent , "include", path )) 
        
    elif sfmat.type == "light" :
        act_mat = []
        TYPE_meshlight_name = name
        
        indent += 1
        #diffuse channel        
        act_mat.append("%s %s %s" %(space* indent , "emit  ", "{")) 
        indent += 1
        act_mat.append("%s %s %s" %(space* indent , '"sRGB nonlinear"', tr_color_str( sfmat.diffuseColor) )) 
        act_mat.append("%s %s %s" %(space* indent , "}", "" )) 
        indent -= 1
        
        act_mat.append("%s %s %s" %(space* indent , "radiance", "%+0.4f" %(sfmat.lightRadiance )  )) 
        act_mat.append("%s %s %s" %(space* indent , "samples ", sfmat.lightSamples )) 
        indent -= 1
        TYPE_meshlight =  True
    
    
    report = {}
    report['light'] = TYPE_meshlight
    report['lightname'] = TYPE_meshlight_name
    report['shader'] = name
    report['defenition'] = act_mat[:]
    del act_mat
    
    return report
        
    

def getShadersInScene():
    scene_mat = bpy.data.materials
    for mat in scene_mat:
        #print(mat.name)
        if mat.users <= 0 :
            print("Material has no owner")
            continue
        if mat.get('sunflow_material') is None:
            print("Not sunflow material")
            continue

        create_shader_block(mat)
            
        #=======================================================================
        # 
        # 
        # # TYPE
        # 'type',
        # # CONST
        # 'diffuseColor',
        # 'constantEmit',
        # 'uberDiffBlend',
        # # DIFF
        # #--------------------------------------------------- 'diffuseColor',
        # # PHON
        # #--------------------------------------------------- 'diffuseColor',
        # 'specularColor',
        # ['phongSamples',
        # 'phongSpecHardness'],
        # # SHIN
        # #--------------------------------------------------- 'diffuseColor',
        # 'shinyReflection',
        # 'shinyExponent',
        # # GLAS
        # 'glassETA',
        # #--------------------------------------------------- 'diffuseColor',
        # 'glassAbsDistance',
        # 'glassAbsColor',
        # # MIRR
        # 'mirrorReflection',
        # # WARD
        # #--------------------------------------------------- 'diffuseColor',
        # #-------------------------------------------------- 'specularColor',
        # ['wardRoughX',
        # 'wardRoughY'],
        # 'wardSamples',
        # # AO
        # 'ambientBright',
        # 'ambientDark',
        # ['ambientSamples',
        # 'ambientDistance'],
        # #UBER
        # #--------------------------------------------------- 'diffuseColor',
        # 
        # #-------------------------------------------------- 'specularColor',
        # 'uberSpecBlend',
        # 'uberGlossy',
        # 'uberSamples',
        # # LIGHT
        # #--------------------------------------------------- 'diffuseColor',
        # 'lightRadiance',
        # 'lightSamples',
        # # JANI
        # 'janinoPath',
        # 
        #=======================================================================
        
        

def working():
    getShadersInScene()


if __name__ == '__main__':
    working()