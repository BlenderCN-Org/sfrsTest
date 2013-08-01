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
# --------------------------------------------------------------------------

import os
import time

import bpy
import mathutils


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


def write_file(filepath, objects, scene,):
    """
    Basic write function. The context and options must be already set
    """
    
    # Flags
    EXPORT_TRI=True
    EXPORT_EDGES=True
    EXPORT_SMOOTH_GROUPS=True
    EXPORT_NORMALS=True
    EXPORT_UV=True
    EXPORT_BEZIER_PATCHES=True
    EXPORT_APPLY_MODIFIERS=True
    EXPORT_KEEP_VERT_ORDER=False
    EXPORT_GLOBAL_MATRIX=None
    
    
    

    if EXPORT_GLOBAL_MATRIX is None:
        EXPORT_GLOBAL_MATRIX = mathutils.Matrix()

    def veckey3d(v):
        return round(v.x, 6), round(v.y, 6), round(v.z, 6)

    #===========================================================================
    # def veckey2d(v):
    #    return round(v[0], 6), round(v[1], 6)
    #===========================================================================

    def veckey2d(v):
        x,y = v
        return "%+0.4f  %+0.4f " %(x,y)

    print('OBJ Export path: %r' % filepath)

    time1 = time.time()

    file_out = open(filepath, "w", encoding="utf8", newline="\n")
    fw = file_out.write

    # Write Header
    fw('/* Blender v%s OBJ File: %r\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)))
    fw('   http://sunflow.sourceforge.net/ */\n')


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

        for ob, ob_mat in obs:
            
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

            # Create the temp file for obj data here
            
            
            print("---------------------------verts---------------------------")
            
            # Vert
            for v in me_verts:
                fw('v %.6f %.6f %.6f\n' % v.co[:])
                print("%+0.4f  %+0.4f %+0.4f "% v.co[:])
                
            print("---------------------------faces---------------------------")
            
            for face , f_index in face_index_pairs:
                print ("%s %s %s "%(face.vertices[:] ))
            
                
                

             
            # UV
            if faceuv:
                facevarying = [None]*len(face_index_pairs)
                for f, f_index in face_index_pairs:
                    store = []
                    for dummy_index, l_index in enumerate(f.loop_indices):
                        uv = uv_layer[l_index].uv 
                        uvkey = veckey2d(uv)
                        store.append(uvkey)
                    rep = ''.join(store)
                    facevarying[f_index] = rep



                for f, f_index in face_index_pairs:
                    print(facevarying[f_index])

                         
            print("---------------------------normals---------------------------")
                 
            # NORMAL, Smooth/Non smoothed.
            if EXPORT_NORMALS:
                for f, f_index in face_index_pairs:
                    if f.use_smooth:
                        face_vertex = []
                        for v_idx in f.vertices:
                            v = me_verts[v_idx]
                            noKey = veckey3d(v.normal)                            
                            face_vertex.append(('%+0.4f %+0.4f %+0.4f' % noKey))                            
                        print('%s %s %s' % (face_vertex[0],face_vertex[1],face_vertex[2]))
                    else:
                        # Hard, 1 normal from the face.
                        noKey = veckey3d(f.normal)
                        expand = ('%+0.4f %+0.4f %+0.4f' % (noKey))              
                        print(" %s %s %s " %(expand,expand,expand))
                            
                            
            print("---------------------------matIndex---------------------------")
            # MATERIAL INDEX
            if len(materials) > 1:
                for f, f_index in face_index_pairs:
                    face_material_index = f.material_index
                    print("%d" %face_material_index)
                                         

            if not faceuv:
                f_image = None
                
            # clean up
            bpy.data.meshes.remove(me)

        if ob_main.dupli_type != 'NONE':
            ob_main.dupli_list_clear()

    file_out.close()

 
    # copy all collected files.

    print("OBJ Export time: %.2f" % (time.time() - time1))


def _write(context, filepath,
              EXPORT_SEL_ONLY,  # should go to another module
              EXPORT_ANIMATION, # should go to another module
              ):  # Not used

    #base_name, ext = os.path.splitext(filepath)
    working_directory, current_blend_file = os.path.split(filepath)
    #------------ current_file_name , extension =  current_blend_file.split('.')
    
    # create a folder inside working directory named 'sunflow_scene'
    # if exist ok
    # if not writable
    # throw error 
    
    # sc names as follows 
    # scene name + frame name + .sc
    # 'include_(above name)'
    
    
    base_name = os.path.join(working_directory, 'sunflow_scene\\' )
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
        write_file(full_path, objects, scene, )

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
    use_animation=False
    
    _write(context, filepath,
           EXPORT_SEL_ONLY=use_selection,
           EXPORT_ANIMATION=use_animation,
           )


if __name__ == '__main__':
    CALL_exporter()