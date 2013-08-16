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
# Created on                          31-Jul-2013
# Author                              NodeBench
#                                    This code is heavily edited version of 
#                                    blender's original wavefront 
#                                    obj exporter code so thanks and 
#                                    credits goes to blender developers 
#                                    and the obj exporter author 
#                                    Campbell Barton
# --------------------------------------------------------------------------

import os
import time

import bpy
import math
import mathutils



#===============================================================================
# getMotionBlurMatrices
#===============================================================================
def getMotionBlurMatrices(scene=None, object_name=None, steps=0, as_matrix=True):
    current_frame , current_subframe = (scene.frame_current, scene.frame_subframe)
    mb_start = current_frame - math.ceil(steps / 2) + 1
    frame_steps = [ mb_start + n for n in range(0, steps) ]
    ref_matrix = None
    animated = False
    matrices = [] 
    obj = scene.objects[object_name]
    base_matrix = obj.matrix_world.copy()
    invert_matrix = base_matrix.inverted()    
    for sub_frame in frame_steps:
        scene.frame_set(sub_frame, current_subframe)
        obj = scene.objects[object_name]
        
        sub_matrix = obj.matrix_world.copy()
        
        sub_matrix = invert_matrix * sub_matrix
        
        if ref_matrix == None:
            ref_matrix = sub_matrix
        animated |= sub_matrix != ref_matrix
        matrx = MatixToList(sub_matrix)
        matrices.append(matrx)
    scene.frame_set(current_frame, current_subframe)
    if not animated:
        matrices = []
    return matrices
                 
#===============================================================================
# getPos
#===============================================================================
def MatixToList(obj_mat):
    matrix_rows = [ "%+0.4f" % element for rows in obj_mat for element in rows ]
    return (matrix_rows)
    


def name_compat(name):
    if name is None:
        return 'None'
    else:
        return name.replace(' ', '_')


def mesh_triangulate(me):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()


def save_object_data(Object_data_name="", Object_data_count=0, Object_data={}, tmpdir_path=""):
    
    print(tmpdir_path)
    #===========================================================================
    # 
    print("""
            object {
                shader "Material"
                type generic-mesh
                name %s""" % Object_data_name)

    #===========================================================================
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
        # print("Object has no uv's defined")
        uv_type = 'none'
    
   
    if 'matindex' in Object_data.keys()  and Object_data['matindex'] != [] :
        if len(Object_data['matindex']) != number_of_faces :
            print("Number of matindex's and faces don't match")
            return
        matindex_type = 'face_shaders'
    else:
        # print("Object has no face shaders's defined")
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
    
    print("}")
    
    
    
    
    
    
    
def write_file(filepath, objects, scene,):
    """
    Basic write function. The context and options must be already set
    """
    
    # Flags
    EXPORT_TRI = True
    EXPORT_EDGES = True
    EXPORT_SMOOTH_GROUPS = True
    EXPORT_NORMALS = True
    EXPORT_UV = True
    EXPORT_BEZIER_PATCHES = True
    EXPORT_APPLY_MODIFIERS = True
    EXPORT_KEEP_VERT_ORDER = False
    EXPORT_GLOBAL_MATRIX = None
    


    if EXPORT_GLOBAL_MATRIX is None:
        EXPORT_GLOBAL_MATRIX = mathutils.Matrix()

    def veckey3d(v):
        return round(v.x, 6), round(v.y, 6), round(v.z, 6)

    def veckey2d(v):
        return round(v[0], 6), round(v[1], 6)

    #===========================================================================
    # def veckey2d(v):
    #    x,y = v
    #    return "%+0.4f  %+0.4f " %(x,y)
    #===========================================================================

    time1 = time.time()


    # Get all meshes
    for ob_main in objects:

        # ignore dupli children
        if ob_main.parent and ob_main.parent.dupli_type in {'VERTS', 'FACES'}:
            # XXX
            print(ob_main.name, 'is a dupli child - ignoring')
            continue

        obs = []
        if ob_main.dupli_type != 'NONE':
            # XXX
            print('creating dupli_list on', ob_main.name)
            ob_main.dupli_list_create(scene)

            obs = [(dob.object, dob.matrix) for dob in ob_main.dupli_list]

            # XXX debug print
            print(ob_main.name, 'has', len(obs), 'dupli children')
        else:
            obs = [(ob_main, ob_main.matrix_world)]

        Object_data_count = 0
        Object_data_name = ob_main.name
        # print("Object is %s" % Object_data_name)
        
        for ob, ob_mat in obs:
            
            Object_data = {}
            Object_data_count += 1
            
            #===================================================================
            # # Bezier Patches supported on sunflow implement here
            # if EXPORT_BEZIER_PATCHES and test_bezier_compat(ob):
            #    ob_mat = EXPORT_GLOBAL_MATRIX * ob_mat
            #    totverts += write_bezier(fw, ob, ob_mat)
            #    continue
            # # END Bezier
            #===================================================================
            
            try:
                me = ob.to_mesh(scene, EXPORT_APPLY_MODIFIERS, 'PREVIEW', calc_tessface=False)
            except RuntimeError:
                me = None

            if me is None:
                continue

            me.transform(EXPORT_GLOBAL_MATRIX * ob_mat)

            if EXPORT_TRI:
                # _must_ do this first since it re-allocs arrays
                mesh_triangulate(me)

            if EXPORT_UV:
                faceuv = len(me.uv_textures) > 0
                if faceuv:
                    uv_texture = me.uv_textures.active.data[:]
                    uv_layer = me.uv_layers.active.data[:]
            else:
                faceuv = False

            me_verts = me.vertices[:]

            # Make our own list so it can be sorted to reduce context switching
            face_index_pairs = [(face, index) for index, face in enumerate(me.polygons)]
            # faces = [ f for f in me.tessfaces ]

            if EXPORT_EDGES:
                edges = me.edges
            else:
                edges = []

            if not (len(face_index_pairs) + len(edges) + len(me.vertices)):  # Make sure there is somthing to write

                # clean up
                bpy.data.meshes.remove(me)

                continue  # dont bother with this mesh.

            if EXPORT_NORMALS and face_index_pairs:
                me.calc_normals()

            if EXPORT_SMOOTH_GROUPS and face_index_pairs:
                smooth_groups, smooth_groups_tot = me.calc_smooth_groups()
                if smooth_groups_tot <= 1:
                    smooth_groups, smooth_groups_tot = (), 0
            else:
                smooth_groups, smooth_groups_tot = (), 0

            materials = me.materials[:]
            material_names = [m.name if m else None for m in materials]

            # avoid bad index errors
            if not materials:
                materials = [None]
                material_names = [name_compat(None)]


            # Sort by Material, then images
            # so we dont over context switch in the obj file.
            if EXPORT_KEEP_VERT_ORDER:
                pass
            else:
                if faceuv:
                    if smooth_groups:
                        sort_func = lambda a: (a[0].material_index,
                                               hash(uv_texture[a[1]].image),
                                               smooth_groups[a[1]] if a[0].use_smooth else False)
                    else:
                        sort_func = lambda a: (a[0].material_index,
                                               hash(uv_texture[a[1]].image),
                                               a[0].use_smooth)
                elif len(materials) > 1:
                    if smooth_groups:
                        sort_func = lambda a: (a[0].material_index,
                                               smooth_groups[a[1]] if a[0].use_smooth else False)
                    else:
                        sort_func = lambda a: (a[0].material_index,
                                               a[0].use_smooth)
                else:
                    # no materials
                    if smooth_groups:
                        sort_func = lambda a: smooth_groups[a[1] if a[0].use_smooth else False]
                    else:
                        sort_func = lambda a: a[0].use_smooth

                face_index_pairs.sort(key=sort_func)

                del sort_func

            # Export Vertex Data
            Object_data['vertices'] = []
            for v in me_verts:
                coordinate_str = [ "%+0.4f" % coordinate for coordinate in v.co[:] ]
                Object_data['vertices'].append(coordinate_str)
            
            # Export Faces Data
            Object_data['faces'] = []
            for face , f_index in face_index_pairs:
                coordinate_str = [ "%06d" % coordinate for coordinate in face.vertices[:] ]
                Object_data['faces'].append(coordinate_str)
            

            # UV
            if faceuv:
                facevarying = [None] * len(face_index_pairs)
                for f, f_index in face_index_pairs:
                    store = []
                    for dummy_index, l_index in enumerate(f.loop_indices):
                        uv = uv_layer[l_index].uv 
                        uvkey = veckey2d(uv)
                        store.append(uvkey)
                    facevarying[f_index] = store


                # Export UV coordinates 
                Object_data['uv'] = []
                for f, f_index in face_index_pairs:                    
                    coordinate_str = [ "%+0.4f" % coordinate for pair in facevarying[f_index] for coordinate in pair ]
                    Object_data['uv'].append(coordinate_str)

                         
                 
            # NORMAL, Smooth/Non smoothed.
            if EXPORT_NORMALS:
                facenormals = []
                for f, f_index in face_index_pairs:
                    if f.use_smooth:
                        face_vertex = []
                        for v_idx in f.vertices:
                            v = me_verts[v_idx]
                            noKey = veckey3d(v.normal)                            
                            face_vertex.append(noKey)                            
                        facenormals.append(face_vertex)
                    else:
                        # Hard, 1 normal from the face.
                        noKey = veckey3d(f.normal)
                        facenormals.append([noKey, noKey, noKey])
                            
                # Export Normal vector 
                Object_data['normal'] = []
                for n_index in facenormals:                    
                    coordinate_str = [ "%+0.4f" % coordinate for pair in n_index for coordinate in pair ]
                    Object_data['normal'].append(coordinate_str)
                    
                    
                    
                            
            # MATERIAL INDEX
            if len(materials) > 1:
                # Export Normal vector 
                Object_data['matindex'] = []
                for f, f_index in face_index_pairs:
                    coordinate_str = "%02d" % f.material_index 
                    Object_data['matindex'].append(coordinate_str)
                                         
            # f_images
            if not faceuv:
                f_image = None
                
            # clean up
            bpy.data.meshes.remove(me)
            
            # save to temp file
            save_object_data(Object_data_name , Object_data_count , Object_data , tmpdir_path="")

        if ob_main.dupli_type != 'NONE':
            ob_main.dupli_list_clear()
            
        matrices = getMotionBlurMatrices(scene, Object_data_name, steps=5, as_matrix=True)
        for each in matrices:
            x = ' '.join(each)
            print("row %s" % x)

 
    # copy all collected files.
    print("OBJ Export time: %.2f" % (time.time() - time1))


#------------------------------------------------------------------------------ 
#===============================================================================
# 
#    print('OBJ Export path: %r' % filepath)
#    
#    file_out = open(filepath, "w", encoding="utf8", newline="\n")
#    fw = file_out.write
# 
#    # Write Header
#    fw('/* Blender v%s OBJ File: %r\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)))
#    fw('   http://sunflow.sourceforge.net/ */\n')
# 
#    file_out.close()
#===============================================================================




















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
