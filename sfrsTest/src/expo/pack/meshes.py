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
import mathutils
# Framework libs
from extensions_framework import util as efutil


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

    # FIXME: object visible ?? hide_render ???
    
def write_mesh_file(objects_namelist, scene, Donot_Allow_Instancing=True , Points_And_Faces=False):
    """
    Basic Mesh Export function. This will directly write to a temp file. 
    And return a list of temp files.
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
    
    return_dict = {}

    if EXPORT_GLOBAL_MATRIX is None:
        EXPORT_GLOBAL_MATRIX = mathutils.Matrix()

    def veckey3d(v):
        return round(v.x, 6), round(v.y, 6), round(v.z, 6)

    def veckey2d(v):
        return round(v[0], 6), round(v[1], 6)

    time1 = time.time()


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
                # XXX
                print('creating dupli_list on', ob_main.name)
                ob_main.dupli_list_create(scene)
    
                obs = [(dob.object, dob.matrix) for dob in ob_main.dupli_list]
    
                # XXX debug print
                print(ob_main.name, 'has', len(obs), 'dupli children')
            else:
                obs = [(ob_main, ob_main.matrix_world)]
        else:  # Allow_Instancing
            obs = [(ob_main, ob_main.matrix_world)]


        for ob, ob_mat in obs:
            
            Object_name = ob.name
            Object_data = {}
            
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
                
            Object_data['material_names'] = material_names[:]

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
            filename = save_object_data(Object_name , Object_data , Only_Points_And_Faces)
            if filename != '':
                item = {}
                item['materials'] = Object_data['material_names']
                item['modifiers'] = []
                item['objectfile'] = filename
                return_dict['Object_name'] = item.copy()
                del item
                del Object_data
                
        if ob_main.dupli_type != 'NONE':
            ob_main.dupli_list_clear()

 
    # copy all collected files.
    print("OBJ Export time: %.2f" % (time.time() - time1))
    return return_dict


def save_object_data(Object_name="", Object_data={}, Points_And_Faces=False):
    
    
    if 'vertices' in Object_data.keys() and Object_data['vertices'] != [] :
        number_of_vertices = len(Object_data['vertices'])
    else:
        print("Object has no vertices")
        return ''
    
    if 'faces' in Object_data.keys() and Object_data['faces'] != [] :
        number_of_faces = len(Object_data['faces'])
    else:
        print("Object has no faces")
        return ''
    
    if  'normal' in Object_data.keys() and Object_data['normal'] != [] :
        if len(Object_data['normal']) != number_of_faces :
            print("Number of normal vector and faces don't match")
            return ''
        normal_type = 'facevarying'
    else:
        print("Object has no normal vector")
        normal_type = 'none'
    
    if 'uv' in Object_data.keys()  and Object_data['uv'] != [] :
        if len(Object_data['uv']) != number_of_faces :
            print("Number of uv's and faces don't match")
            return ''
        uv_type = 'facevarying'
    else:
        print("Object has no uv's defined")
        uv_type = 'none'
    
   
    if 'matindex' in Object_data.keys()  and Object_data['matindex'] != [] :
        if len(Object_data['matindex']) != number_of_faces :
            print("Number of matindex's and faces don't match")
            return ''
        matindex_type = 'face_shaders'
    else:
        print("Object has no face shaders's defined")
        matindex_type = ''
        
    
#------------------------------------------------------------------------------ 
    act_obj = []
    indent = 0
    space = "        "
    indent += 1
    
    
    act_obj.append("%s %s %s" % (space * indent , "points", number_of_vertices))
    indent += 1
    for item in Object_data['vertices']:
        vertstring = '  '.join(item)
        act_obj.append("%s %s %s" % (space * indent , "", vertstring))
    indent -= 1
    
    act_obj.append("%s %s %s" % (space * indent , "triangles", number_of_faces))
    indent += 1
    for item in Object_data['faces']:
        facestring = '  '.join(item)
        act_obj.append("%s %s %s" % (space * indent , "", facestring))
    indent -= 1
    
    if not Points_And_Faces:
        act_obj.append("%s %s %s" % (space * indent , "normals", normal_type))
        if normal_type == 'none':        
            pass
        else:        
            indent += 1
            for item in Object_data['normal']:
                concat = ' '.join(item)
                act_obj.append("%s %s %s" % (space * indent , "", concat))
            indent -= 1    
    
    if not Points_And_Faces:
        act_obj.append("%s %s %s" % (space * indent , "uvs", uv_type))
        if uv_type == 'none':        
            pass
        else:        
            indent += 1
            for item in Object_data['uv']:
                concat = ' '.join(item)
                act_obj.append("%s %s %s" % (space * indent , "", concat))
            indent -= 1
    
    if not Points_And_Faces:
        act_obj.append("%s %s %s" % (space * indent , "", matindex_type))
        if uv_type == 'none':        
            pass
        else:        
            indent += 1
            for item in Object_data['matindex']:
                act_obj.append("%s %s %s" % (space * indent , "", item))
            indent -= 1        
        indent -= 1

#------------------------------------------------------------------------------ 

    tmpfile = efutil.temp_file(Object_name)
    outfile = open(tmpfile, 'w')
    for lines in act_obj :
        outfile.write("\n%s" % lines)
    outfile.close()
    print("tmpfile>> %s" % tmpfile)
    return tmpfile
