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
    
def InstanceExporter(scene , objname, turn_on_motion_blur, steps=0):
    if not turn_on_motion_blur:
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
            dupli_list[ ins['iname'] ] = ins
        obj_parent.dupli_list_clear()
        return dupli_list
    else:
        obj_parent = scene.objects[objname]
        obj_parent.dupli_list_create(scene)
        num_dupli = len(obj_parent.dupli_list)
        dupli_list = {}
        for obj in obj_parent.dupli_list :
            ins = {}  
            ins['iname'] = "%s.inst.%03d" % (obj_parent.name, obj.index)
            ins['index'] = obj.index
            ins['pname'] = obj.object.name
            ins['trans'] = None
            dupli_list[ ins['iname'] ] = ins
        obj_parent.dupli_list_clear()
        
        current_frame , current_subframe = (scene.frame_current, scene.frame_subframe)
        mb_start = current_frame - math.ceil(steps / 2) + 1
        frame_steps = [ mb_start + n for n in range(0, steps) ]
        transform = [ [] for dummy_i in range(num_dupli)] 
        for sub_frame in frame_steps:
            scene.frame_set(sub_frame, current_subframe)            
            obj_parent.dupli_list_create(scene)
            for objindx in range(num_dupli) :
                xpos = getPos(obj_parent.dupli_list[objindx], as_matrix=True)
                transform[objindx].append(xpos)
            obj_parent.dupli_list_clear()
        scene.frame_set(current_frame, current_subframe)

        for dup in dupli_list.values():
            if obj_parent.dupli_type == 'FRAMES':
                dup['trans'] = transform[dup['index'] - obj_parent.dupli_frames_start ]
            else:
                dup['trans'] = transform[dup['index']]            
        return dupli_list
        
        
def sceneObjectsExporter(ObjectsRepository={}, Export_instances=False):  
    # loop through the objects in the scene
    # create a dictionary
    # mark non exportable objects like light, camera, lightmat , *empty
    
    scene = bpy.context.scene
    
    # filter objects - avoid camera , lamp
    obj_lst = [ obj.name  for obj in scene.objects if obj.type not in ['CAMERA', 'LAMP'] ]

    
    # filter objects - avoid meshlights ; these are not objects but lights    
    nonlights = [obj for obj in obj_lst if obj not in ObjectsRepository['MeshLightObjects'].keys() ]
    del obj_lst
    obj_lst = nonlights
    
    if Export_instances:
        proxy_list = {}
        
        for objname in obj_lst:
            turn_on_motion_blur = True
            mblur_steps = 5
            if objname in ObjectsRepository['MotionBlurObjects'].keys() :
                mblur_steps = 5
                turn_on_motion_blur = True        
            cur_object = scene.objects[objname]

            
            if (
                (cur_object.is_duplicator) & 
                (cur_object.children != ()) & 
                (cur_object.dupli_type in ['VERTS' , 'FACES' ]) 
                ):
                dupli_list = InstanceExporter(scene , objname , turn_on_motion_blur , mblur_steps)
                dmix(ObjectsRepository, dupli_list, 'Instances')
                proxy_list[objname] = True
                print ("Instantiated>> %s" % objname)
            if (
                (cur_object.is_duplicator) & 
                (cur_object.children == ()) & 
                (cur_object.dupli_type in ['GROUP' , 'FRAMES']) 
                ):
                dupli_list = InstanceExporter(scene , objname , turn_on_motion_blur , mblur_steps)
                dmix(ObjectsRepository, dupli_list, 'Instances')
                proxy_list[objname] = True
                print ("Instantiated>> %s" % objname)
            dmix(ObjectsRepository, proxy_list, 'Instantiated')
            
            
        # filter objects - avoid instances ;         
        noninst = [obj for obj in obj_lst if obj not in ObjectsRepository['Instantiated'].keys() ]
        del obj_lst
        obj_lst = noninst 
        # print(obj_lst)   
    
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
            # print (each)
            pass
            
            
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
            ln = len(inst['trans'])
            if ln == 1:
                act_inst.append("%s %s %s" % (space * indent , "transform  row", ' '.join(inst['trans'][0])))
            else:
                act_inst.append("%s %s %s" % (space * indent , "transform", ""))
                act_inst.append("%s %s %s" % (space * indent , "steps", 5))
                act_inst.append("%s %s %s" % (space * indent , "times", "0 1"))                
                for exh in range(ln):
                    act_inst.append("%s %s %s" % (space * indent , "row", ' '.join(inst['trans'][exh])))                
            act_inst.append("%s %s %s" % (space * indent , "shader", "Material.shader"))
            indent -= 1 
            act_inst.append("%s %s %s" % (space * indent , "}", ""))
            # act_inst.append("%s %s %s" % (space * indent , "modifier", " "))
    instfile = open("E:\Graphics\Works\\testbuildsfor253\DupliesTest\Objects.ins.sc" , 'w')
    for x in act_inst:
        instfile.write("\n%s" % x)
    instfile.close()
    #===========================================================================


if __name__ == '__main__':
    getListInstances()
