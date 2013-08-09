'''
Created on 10-Aug-2013

@author: AppleCart
'''


import bpy
import math

def getTrans():
    m = bpy.context.scene.objects['EmptyActor'].matrix_world
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




def getOBJ():
    print (bpy.context.scene.objects[:])


if __name__ == '__main__':
    getTrans()