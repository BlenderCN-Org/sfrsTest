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

import bpy
import math
import mathutils


def getDepthOfField(camera , EmptyActor):
    cam = camera.matrix_world.copy()
    foc = EmptyActor.matrix_world.copy()
    cam.transpose()
    foc.transpose()
    cam_pos = cam[3]
    cam_dir = cam[2]
    foc_pos = foc[3]
    cam_foc = foc_pos - cam_pos
    dist = cam_foc.dot(cam_dir)
    perpendicular_distance = round(dist,5)
    direct_distance = cam_foc.length
    return (abs(perpendicular_distance), direct_distance)    

    
def calculateDOF(camera, dof_object, scene):
    if dof_object.name in [ obj.name for obj in scene.objects ]:
        return getDepthOfField(camera, dof_object)
    else:
        return ( 0.0 , 0.0 )


def getCameraPos(obj, as_matrix = True):
    obj_mat = obj.matrix_world.copy()
    if not as_matrix :
        obj_mat.transpose()
        eye = obj_mat[3]
        dir = obj_mat[2]
        up  = obj_mat[1]
        target = eye - dir        
        points = [ eye.to_tuple()[:3], target.to_tuple()[:3], up.to_tuple()[:3] ]        
        pos = [ "%+0.4f %+0.4f %+0.4f" % elm for elm in points ]
        return ( pos )
    else:
        matrix_rows =[ "%+0.4f" %element for rows in obj_mat for element in rows ]
        return ( matrix_rows )
        

def getCameraMotionBlurMatrices(scene =None, camera =None, steps =0, as_matrix = True):
    current_frame ,current_subframe = (scene.frame_current,scene.frame_subframe)
    mb_start = current_frame - math.ceil(steps/2) +1
    frame_steps =  [ mb_start + n for n in range( 0, steps) ]
    matrices = [] 
    for sub_frame in frame_steps:
        scene.frame_set(sub_frame, current_subframe)
        obj = scene.objects['Camera']
        matrices.append(getCameraPos(obj, as_matrix))
    scene.frame_set(current_frame, current_subframe)
    return matrices
                 


def getActiveCamera(scene=None):
    CameraData = {}
    act_cam = [] 
    indent = 0
    space = "        "
    as_matrix = False
    camera = scene.camera   #this should be the active camera in blender
    if camera is not None:
        
        #Export    
        cam = camera.data.sunflow_camera
        fov = math.degrees(camera.data.angle)
        aspect = float(scene.render.resolution_x ) / float (scene.render.resolution_y)
        shift =  (camera.data.shift_x , camera.data.shift_y) 
        position = getCameraPos( camera, as_matrix )
            
        if cam.cameraMBlur:
            matrices = getCameraMotionBlurMatrices(scene, camera, cam.cameraMBlurSteps, as_matrix )

        
        fdist = 0.0
        if cam.cameraType == "thinlens" and cam.dofEnabledScene and camera.data.dof_object is not None:
            fdist , direct = calculateDOF(camera, camera.data.dof_object , scene)
        lensr = "%+0.4f" %cam.aperture
        sides = cam.apertureBlades
        rotation = "%+0.4f" %cam.bladeRotation
            
        
        
        act_cam.append("%s %s %s" %(space* indent , "camera", "{"))
        indent +=1
        act_cam.append("%s %s %s" %(space* indent , "type" , cam.cameraType))
        
        if cam.cameraType in [ "pinhole" , "thinlens" ]:            
            if ( cam.objectMBlur | cam.cameraMBlur ):
                act_cam.append("%s %s %s" %(space* indent , "shutter", "0 1"))
            if cam.cameraMBlur :
                act_cam.append("%s %s %s" %(space* indent , "steps", cam.cameraMBlurSteps))
                act_cam.append("%s %s %s" %(space* indent , "times", "0 1"))                
                if as_matrix:
                    indent += 1
                    for matrixtransform in matrices:
                        mat_to_string = ' '.join(matrixtransform)
                        act_cam.append("%s %s %s" %(space* indent , "transform  row", mat_to_string))
                    indent -= 1
                else:
                    for matrixtransform in matrices:
                        indent += 1
                        (eye,target,up) = matrixtransform
                        act_cam.append("%s %s %s" %(space* indent , "{", ""))
                        act_cam.append("%s %s %s" %(space* indent , "eye   ", eye))
                        act_cam.append("%s %s %s" %(space* indent , "target", target))
                        act_cam.append("%s %s %s" %(space* indent , "up    ", up))
                        act_cam.append("%s %s %s" %(space* indent , "}", ""))
                        indent -= 1
            else:
                if as_matrix:
                    mat_to_string = ' '.join(position)
                    act_cam.append("%s %s %s" %(space* indent , "transform  row", mat_to_string))
                else:
                    (eye,target,up) = position
                    act_cam.append("%s %s %s" %(space* indent , "eye   ", eye))
                    act_cam.append("%s %s %s" %(space* indent , "target", target))
                    act_cam.append("%s %s %s" %(space* indent , "up    ", up))
                    
            act_cam.append("%s %s %s" %(space* indent , "fov   ", round(fov,5)  ))              
            act_cam.append("%s %s %s" %(space* indent , "aspect", round(aspect,5)  )) 
            
            if ( shift ) != (0.0,0.0):
                act_cam.append("%s %s %s" %(space* indent , "shift", "%+0.4f %+0.4f" %shift )) 
                
        if (cam.cameraType == "thinlens"):
            if cam.dofEnabledScene :
                act_cam.append("%s %s %s" %(space* indent , "fdist", fdist)) 
                act_cam.append("%s %s %s" %(space* indent , "lensr", lensr)) 
                if sides > 3 :
                    act_cam.append("%s %s %s" %(space* indent , "sides", sides)) 
                    act_cam.append("%s %s %s" %(space* indent , "rotation", rotation)) 
        elif cam.cameraType in ["spherical" ,"fisheye"]:
            if as_matrix:
                mat_to_string = ' '.join(position)
                act_cam.append("%s %s %s" %(space* indent , "transform  row", mat_to_string))
            else:
                (eye,target,up) = position
                act_cam.append("%s %s %s" %(space* indent , "eye   ", eye))
                act_cam.append("%s %s %s" %(space* indent , "target", target))
                act_cam.append("%s %s %s" %(space* indent , "up    ", up))
        else:
            pass 
        
        act_cam.append("%s %s %s" %(space* indent , "}", ""))   
        indent -=1
        #end_Export
  
        CameraData['camera'] = camera.name
        CameraData['cameradata'] = act_cam
        CameraData['cameramblur'] = cam.cameraMBlur
        CameraData['objectmblur'] = cam.objectMBlur
        CameraData['objectmblurgroup'] = cam.objectMBlurGroupName
        
    return CameraData


if __name__ == '__main__':
    import time
    ti = time.time()
    scene = bpy.context.scene
    test_dict = getActiveCamera(scene)
    for each in test_dict['cameradata']:
        print(each)
    print("Export time: %.2f" % (time.time() - ti))