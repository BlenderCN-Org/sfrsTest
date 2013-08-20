'''
Created on 20-Aug-2013
@author: AppleCart
'''

import random

file_ = r"E:\Graphics\Render\testparticles\_include.Scene.001\particle.sc"


def writeout(asset, m):
    fl = open(file_, m)
    for lines in asset:
        fl.write("\n%s" % lines)    
    fl.close()

def generate():
    asset = []
    indent = 0
    space = "        "
    part_points = []
    num_point = 2000  # 200000
    
    limit = 3
    

    
    asset.append("%s %s %s" % (space * indent , "object", "{")) 
    indent += 1
    asset.append("%s %s %s" % (space * indent , "shader", "Material.001"))
    asset.append("%s %s %s" % (space * indent , "type", "particles"))
    asset.append("%s %s %s" % (space * indent , "points", num_point))
    writeout(asset, 'w')
    indent += 1
    step = num_point / 1000
    n = 0
    for x in xrange(step):
        asset = []
        # print("step %s" % x)
        for each in xrange(1000):
            
            ut = [ (limit - (2 * limit * random.random())) for x in range(3) ] 
            pt = "  %+0.4f  %+0.4f  %+0.4f" % (ut[0], ut[1], ut[2])
            asset.append("%s %s %s" % (space * indent , "", pt))
        writeout(asset, 'a')     
    asset = []   
    indent -= 1
    asset.append("%s %s %s" % (space * indent , "radius ", "0.1"))
    indent -= 1
    asset.append("%s %s %s" % (space * indent , "}", ""))    
    writeout(asset, 'a')
    print("Finished %s" % n)

if __name__ == '__main__':
    generate()
