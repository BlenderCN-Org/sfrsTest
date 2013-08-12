'''
Created on 10-Aug-2013
@author: AppleCart
'''


import bpy
import math

def getTrans():
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





def getCameraPos(obj, as_matrix = True):
    obj_mat = obj.matrix_world.copy()
    if not as_matrix :
        obj_mat.transpose()
        eye = obj_mat[3]
        dir = obj_mat[2]
        up  = obj_mat[1]
        target = eye - dir
        print  ("{")
        print  ("        eye     %+0.4f %+0.4f %+0.4f" %eye.to_tuple(5)[:3] )
        print  ("        target  %+0.4f %+0.4f %+0.4f" %target.to_tuple(5)[:3] )
        print  ("        up      %+0.4f %+0.4f %+0.4f" %up.to_tuple(5)[:3] )
        print  ("}")
    else:
        matrix_rows = '  '.join([ "%+0.4f" %element for rows in obj_mat for element in rows ])
        print ("    transform  row %s" %matrix_rows )
        
                
    

def getSceneCameraPos():
    C = bpy.context
    steps = 5
    print  ("steps  %d" %steps)
    print  ("times 0.0 1.0")
    current_frame ,current_subframe = (C.scene.frame_current,C.scene.frame_subframe)
    #print( "current_frame " + str(current_frame) + " current_subframe " + str(current_subframe)) 
    mb_start = current_frame - math.ceil(steps/2) +1

    frame_steps =  [ mb_start + n for n in range( 0, steps) ] 

    for sub_frame in frame_steps:
        C.scene.frame_set(sub_frame, current_subframe)
        obj = C.scene.objects['Camera']
        getCameraPos(obj)
    C.scene.frame_set(current_frame, current_subframe)
        





def getOBJ():
    print (bpy.context.scene.objects[:])


if __name__ == '__main__':
    getSceneCameraPos()