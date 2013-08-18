'''
Created on 14-Aug-2013

@author: AppleCart
'''





def save_object_data(Object_data_name="", Object_data_count=0, Object_data={}, tmpdir_path=""):
    
    print(tmpdir_path)
    
    if 'vertices' in Object_data.keys() and Object_data['vertices'] != [] :
        number_of_vertices = len(Object_data['vertices'])
    else:
        print("Object has no vertices")
        return
    
    if 'faces' in Object_data.keys() and Object_data['faces'] != [] :
        number_of_faces = len(Object_data['faces'])
    else:
        print("Object has no faces")
        return
    
    if  'normal' in Object_data.keys() and Object_data['normal'] != [] :
        if len(Object_data['normal']) != number_of_faces :
            print("Number of normal vector and faces don't match")
            return
        normal_type = 'facevarying'
    else:
        print("Object has no normal vector")
        normal_type = 'none'
    
    if 'uv' in Object_data.keys()  and Object_data['uv'] != [] :
        if len(Object_data['uv']) != number_of_faces :
            print("Number of uv's and faces don't match")
            return
        uv_type = 'facevarying'
    else:
        print("Object has no uv's defined")
        uv_type = 'none'
    
   
    if 'matindex' in Object_data.keys()  and Object_data['matindex'] != [] :
        if len(Object_data['matindex']) != number_of_faces :
            print("Number of matindex's and faces don't match")
            return
        matindex_type = 'face_shaders'
    else:
        print("Object has no face shaders's defined")
        matindex_type = ''
        
        
    TAB = '    '
    indent = 0
    
    indent += 1
    print("%s %s %d" % (TAB * indent , 'points' , number_of_vertices))
    
    indent += 1
    for item in Object_data['vertices']:
        print("%s %s %s %s" % (TAB * indent , item[0] , item[1] , item[2]))
    indent -= 2
    
    
    indent += 1
    print("%s %s %d" % (TAB * indent , 'triangles' , number_of_faces))
    
    indent += 1
    for item in Object_data['faces']:
        print("%s  %s  %s  %s" % (TAB * indent , item[0] , item[1] , item[2]))
    indent -= 2
    
    indent += 1
    print("%s %s %s" % (TAB * indent , 'normals' , normal_type))
    if normal_type == 'none':        
        indent -= 1
    else:        
        indent += 1
        for item in Object_data['normal']:
            concat = ' '.join(item)
            print("%s %s" % (TAB * indent , concat))
        indent -= 2

    indent += 1
    print("%s %s %s" % (TAB * indent , 'uvs' , uv_type))
    if uv_type == 'none':        
        indent -= 1
    else:        
        indent += 1
        for item in Object_data['uv']:
            concat = ' '.join(item)
            print("%s %s" % (TAB * indent , concat))
        indent -= 2
    
    
    indent += 1
    print("%s %s %s" % (TAB * indent , '' , matindex_type))
    if matindex_type == '':                
        indent -= 1
    else:         
        indent += 1
        for item in Object_data['matindex']:
            print("%s %s" % (TAB * indent , item))
        indent -= 2
    














def _write(context, filepath,
              EXPORT_SEL_ONLY,  # should go to another module
              EXPORT_ANIMATION,  # should go to another module
              ):  # Not used

    # base_name, ext = os.path.splitext(filepath)
    working_directory, current_blend_file = os.path.split(filepath)
    #------------ current_file_name , extension =  current_blend_file.split('.')
    
    # create a folder inside working directory named 'sunflow_scene'
    # if exist ok
    # if not writable
    # throw error 
    
    # sc names as follows 
    # scene name + frame name + .sc
    # 'include_(above name)'
    
    
    base_name = os.path.join(working_directory, 'sunflow_scene\\')
    ext = '.sc'
    context_name = [base_name, 'frame', '', ext]  # Base name, scene name, frame number, extension
    print ("context_name: " + '_'.join(context_name))
    




    scene = context.scene

    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    orig_frame = scene.frame_current

    # Export an animation?
    if EXPORT_ANIMATION:
        scene_frames = range(scene.frame_start, scene.frame_end + 1)  # Up to and including the end frame.
    else:
        scene_frames = [orig_frame]  # Dont export an animation.

    # Loop through all frames in the scene and export.
    for frame in scene_frames:
        if EXPORT_ANIMATION:  # Add frame to the filepath.
            context_name[2] = '_%.6d' % frame

        scene.frame_set(frame, 0.0)
        if EXPORT_SEL_ONLY:
            objects = context.selected_objects
        else:
            objects = scene.objects

        full_path = ''.join(context_name)

        # erm... bit of a problem here, this can overwrite files when exporting frames. not too bad.
        # EXPORT THE FILE.
        write_file(full_path, objects, scene,)

    scene.frame_set(orig_frame, 0.0)

    # Restore old active scene.
#   orig_scene.makeCurrent()
#   Window.WaitCursor(0)


"""
Currently the exporter lacks these features:
* multiple scene export (only active scene is written)
* particles
"""


def CALL_exporter():
    context = bpy.context
    filepath = bpy.data.filepath
    use_selection = False
    use_animation = False
    
    _write(context, filepath,
           EXPORT_SEL_ONLY=use_selection,
           EXPORT_ANIMATION=use_animation,
           )


if __name__ == '__main__':
    CALL_exporter()
