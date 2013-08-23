'''
Created on 21-Aug-2013

@author: AppleCart
'''
import bpy


def getParticleSystem():
#     ob = bpy.context.scene.objects['Plane']
#     mod = ob.modifiers[0]
#     psys = ob.particle_systems[0]
# 
#     steps = psys.settings.draw_step
#     steps = 2 ** steps + 1
#     
#     num_parents = len(psys.particles)
#     num_children = len(psys.child_particles)
#       
#     print("num parents: " + str(num_parents))
#     print("num children: " + str(num_children))
#       
#     for pindex in range(0, num_parents + num_children):
#         print("particle " + str(pindex))
#         for step in range(0, steps):
#             co = psys.co_hair(ob, mod, pindex, step)
#             print("step " + str(step) + ": " + str(co)) 


    import bpy
      
    ob = bpy.context.active_object
    mod = ob.modifiers[0]
    psys = mod.particle_system
      
    steps = psys.settings.draw_step
    steps = 2 ** steps + 1
      
    num_parents = len(psys.particles)
    num_children = len(psys.child_particles)
      
    print("num parents: " + str(num_parents))
    print("num children: " + str(num_children))
      
    for pindex in range(0, num_parents + num_children):
        print("particle " + str(pindex))
        for step in range(0, steps):
            co = psys.co_hair(ob, mod, pindex, step)
            print("step " + str(step) + ": " + str(co))

    

if __name__ == '__main__':
    getParticleSystem()
    
    
    
    
#===============================================================================
# import bpy
#  
# ob = bpy.context.active_object
# mod = ob.modifiers[0]
# psys = mod.particle_system
#  
# steps = psys.settings.draw_step
# steps = 2**steps + 1
#  
# num_parents = len(psys.particles)
# num_children = len(psys.child_particles)
#  
# print("num parents: " + str(num_parents))
# print("num children: " + str(num_children))
#  
# for pindex in range(0, num_parents + num_children):
#     print("particle " + str(pindex))
#     for step in range(0, steps):
#         co = psys.co_hair(ob, mod, pindex, step)
#         print("step " + str(step) + ": " + str(co))
#===============================================================================
