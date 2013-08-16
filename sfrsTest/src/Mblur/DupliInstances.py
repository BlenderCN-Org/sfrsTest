'''
Created on 16-Aug-2013
@author: AppleCart
'''

import bpy
import math
import mathutils


        
#===============================================================================
# getPos
#===============================================================================
def MatixToString(obj_mat, duplis):
    if duplis:
        matrix_rows = [] 
        for each_mat in obj_mat:
            matrix_rows.append([ "%+0.4f" % element for rows in each_mat for element in rows ])
    else:
        matrix_rows = [ "%+0.4f" % element for rows in obj_mat for element in rows ]
    return (matrix_rows)
    


def motion_blur_object(scene , obj_name , duplis , steps):
    current_frame , current_subframe = (scene.frame_current, scene.frame_subframe)
    mb_start = current_frame - math.ceil(steps / 2) + 1
    frame_steps = [ mb_start + n for n in range(0, steps) ]
    ref_matrix = None
    animated = False
    
    obj = scene.objects[obj_name]
    if duplis :
        obj.dupli_list_create(scene)
        len_d = len(obj.dupli_list)
        matrices = []
        base_matrix = [ obj.dupli_list[i].matrix.copy() for i  in  range(len_d) ]
        invert_matrix = [ base_matrix[i].inverted() for i  in  range(len_d) ]
        obj.dupli_list_clear()
    else:
        matrices = [] 
        base_matrix = obj.matrix_world.copy()
        invert_matrix = base_matrix.inverted()   
    inx = 0
    for sub_frame in frame_steps:
        scene.frame_set(sub_frame, current_subframe)
        if duplis :            
            obj = scene.objects[obj_name]
            obj.dupli_list_create(scene)
            sub_matrix_l = [ obj.dupli_list[i].matrix.copy() for i  in  range(len_d) ]
            sub_matrix = [ invert_matrix[i] * sub_matrix_l[i] for i  in  range(len_d) ]
            del sub_matrix_l
            obj.dupli_list_clear()
        else:
            obj = scene.objects[obj_name]
            sub_matrix = obj.matrix_world.copy()        
            sub_matrix = invert_matrix * sub_matrix      
        matrices.append(MatixToString(sub_matrix , duplis))
        inx += 1
    scene.frame_set(current_frame, current_subframe)
    del base_matrix
    return matrices




def testthis():
    scene = bpy.context.scene
    Donot_Allow_Instancing = True
    objects_namelist = ['AloneCube', 'Cube', 'Circle']
    mblurlist = ['Circle']
    steps = 5
    
    # Get all meshes
    for ob_main_name in objects_namelist:

        obs = []
        ob_main = scene.objects[ob_main_name]
                
        if Donot_Allow_Instancing:
            # ignore dupli children
            if ob_main.parent and ob_main.parent.dupli_type in {'VERTS', 'FACES'}:
                # XXX
                print(ob_main.name, 'is a dupli child - ignoring')
                continue

            if ob_main.dupli_type != 'NONE':
                # TODO: need testing on motion blur (parent)
                if ob_main_name in mblurlist: 
                    print("No inst , duplis %s" % ob_main_name)
                    listx = motion_blur_object(scene, ob_main_name, True, steps)
                    # print("length %s" % len(listx))
                    print(listx)
                    
                # XXX
                print('creating dupli_list on', ob_main.name)
                ob_main.dupli_list_create(scene)
    
                obs = [(dob.object, dob.matrix) for dob in ob_main.dupli_list]
    
                # XXX debug print
                print(ob_main.name, 'has', len(obs), 'dupli children')
            else:
                # TODO: need testing on motion blur (normal object / non children non parent)
                if ob_main_name in mblurlist:
                    print("No inst , normal %s" % ob_main_name)
                    print(motion_blur_object(scene, ob_main_name, False, steps))
                obs = [(ob_main, ob_main.matrix_world)]
        else:  # Allow_Instancing
            # TODO: need testing on motion blur (normal object / non children )
            if ob_main_name in mblurlist:
                print("Inst , normal %s" % ob_main_name)
                print(motion_blur_object(scene, ob_main_name, False, steps))
            obs = [(ob_main, ob_main.matrix_world)]

        for ob, ob_mat in obs:            
            print(ob.index)

if __name__ == '__main__':
    testthis()






















