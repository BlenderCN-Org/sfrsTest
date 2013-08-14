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

import bpy
import copy
import math
import mathutils


def dict_merge(*dictionaries):
    cp = {}
    for dic in dictionaries:
        cp.update(copy.deepcopy(dic))
    return cp

def dmix(MasterDict, InputDict , TargetName):
    if TargetName not in MasterDict.keys():
        MasterDict[TargetName] = {}        
    for keys in InputDict.keys():
        MasterDict[TargetName][keys] = InputDict[keys]

def getPos(obj, as_matrix=True):
    obj_mat = obj.matrix.copy()
    matrix_rows = [ "%+0.4f" % element for rows in obj_mat for element in rows ]
    return (matrix_rows)
        
def getMotionBlurMatrices(scene=None, camera=None, steps=0, as_matrix=True):
    current_frame , current_subframe = (scene.frame_current, scene.frame_subframe)
    mb_start = current_frame - math.ceil(steps / 2) + 1
    frame_steps = [ mb_start + n for n in range(0, steps) ]
    matrices = [] 
    for sub_frame in frame_steps:
        scene.frame_set(sub_frame, current_subframe)
        obj = scene.objects['Camera']
        matrices.append(getPos(obj, as_matrix))
    scene.frame_set(current_frame, current_subframe)
    return matrices
                 

def InstanceExporter(scene , objname, turn_on_motion_blur):
    # TODO: motion blur related calculations
    # current_frame = (scene.frame_current , scene.frame_subframe) 
    
    obj_parent = scene.objects[objname]
    obj_parent.dupli_list_create(scene)
    dupli_list = {}
    for obj in obj_parent.dupli_list :
        ins = {}
        pos = getPos(obj, as_matrix=True)   
        ins['iname'] = "%s.inst.%03d" % (obj_parent.name, obj.index)
        ins['index'] = obj.index
        ins['pname'] = obj.object.name
        ins['trans'] = [pos]
        # TODO: try deepcopy here check any performance change
        dupli_list[ ins['iname'] ] = ins
    obj_parent.dupli_list_clear()
    return dupli_list
    
        


def sceneObjectsExporter(ObjectsRepository={}, Export_instances=False):  
    # FIXME: we dont need this as a module
    # loop through the objects in the scene
    # create a dictionary
    # mark non exportable objects like light, camera, lightmat , *empty
    
    scene = bpy.context.scene
    
    # filter objects - avoid camera , lamp
    obj_lst = [ obj.name  for obj in scene.objects if obj.type not in ['CAMERA', 'LAMP'] ]
    print(obj_lst)
    
    # filter objects - avoid meshlights ; these are not objects but lights
    
    nonlights = [obj for obj in obj_lst if obj not in ObjectsRepository['MeshLightObjects'].keys() ]
    del obj_lst
    obj_lst = nonlights
    
    if Export_instances:
        proxy_list = {}
        
        for objname in obj_lst:
            turn_on_motion_blur = False
            if objname in ObjectsRepository['MotionBlurObjects'].keys() :
                turn_on_motion_blur = True        
            cur_object = scene.objects[objname]
            
    #         print(cur_object)
    #         print(cur_object.is_duplicator)
    #         print(cur_object.children)
    #         print(cur_object.dupli_type)
            
            if (
                (cur_object.is_duplicator) & 
                (cur_object.children != ()) & 
                (cur_object.dupli_type in ['VERTS' , 'FACES' ]) 
                ):
                dupli_list = InstanceExporter(scene , objname , turn_on_motion_blur)
                dmix(ObjectsRepository, dupli_list, 'Instances')
                proxy_list[objname] = True
                print ("Instantiated>> %s" % objname)
            dmix(ObjectsRepository, proxy_list, 'Instantiated')
            
            
        # filter objects - avoid instances ; 
        
        noninst = [obj for obj in obj_lst if obj not in ObjectsRepository['Instantiated'].keys() ]
        del obj_lst
        obj_lst = noninst 
        print(obj_lst)   
    
    for objname in obj_lst:
        # ActualsExporter()
        print ("Exported>> %s" % objname)
         

def getListInstances():
    ObjectsRepository = {}
    Export_instances = True
    # ObjectsRepository = { 
    #                       MotionBlurObjects:{},
    #                       MeshLightObjects:{},
    #                       ExportedObjects:{},
    #                       Instances:{},
    #                       Instantiated:{},
    #                    }
    # obj = objname , [material_list] , [modifiers_list] , object_def_file_path
    # inst= instname , actualobject , transteps[]
    
    #===========================================================================
    # test
    ObjectsRepository['MeshLightObjects'] = {}
    ObjectsRepository['MotionBlurObjects'] = {}    
    #===========================================================================
    sceneObjectsExporter(ObjectsRepository, Export_instances)
    
    
    
    #===========================================================================
    # display test
    key = 'Instances'
    if key in ObjectsRepository.keys():
        # print (ObjectsRepository[key])
        for each in ObjectsRepository[key].items():
            print (each)
            
    #===========================================================================
    
    
    #===========================================================================
    # assembler test
    key = 'Instances'
    act_inst = []
    indent = 0
    space = "        "
    if key in ObjectsRepository.keys():
        for keyptr , inst in ObjectsRepository[key].items():
            act_inst.append("%s %s %s" % (space * indent , "instance", "{"))
            indent += 1 
            act_inst.append("%s %s %s" % (space * indent , "name", inst['iname']))
            act_inst.append("%s %s %s" % (space * indent , "geometry", inst['pname']))
            act_inst.append("%s %s %s" % (space * indent , "transform  row", ' '.join(inst['trans'][0])))
            act_inst.append("%s %s %s" % (space * indent , "shader", "Material.shader"))
            indent -= 1 
            act_inst.append("%s %s %s" % (space * indent , "}", ""))
            # act_inst.append("%s %s %s" % (space * indent , "modifier", " "))
    instfile = open("E:\Graphics\Works\\testbuildsfor253\DupliesTest\Objects.ins.sc" , 'w')
    for x in act_inst:
        instfile.write("\n%s" % x)
    instfile.close()
    #===========================================================================


# instance {
#    name nameOfInstance
#    geometry theOriginalObjectName
#    transform {
#       rotatex -90
#       scaleu 1.0
#       translate -1.0 3.0 -1.0
#    }
#    shader shaderForInstance
#    modifier modForInstance
# }


if __name__ == '__main__':
    getListInstances()
