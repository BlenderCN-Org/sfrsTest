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
# Created on                          15-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------



def Assemble_File(ObjectsRepository):

   
    
    key = 'Instances'
    act_inst = []
    indent = 0
    space = "        "
    if key in ObjectsRepository.keys():
        for keyptr , inst in ObjectsRepository[key].items():
            act_inst.append("%s %s %s" % (space * indent , "instance", "{"))
            indent += 1 
            act_inst.append("%s %s %s" % (space * indent , "name", inst['iname']))
            act_inst.append("%s %s %s" % (space * indent , "geometry", inst['pname']))
            ln = len(inst['trans'])
            if ln == 1:
                act_inst.append("%s %s %s" % (space * indent , "transform  row", ' '.join(inst['trans'][0])))
            else:
                act_inst.append("%s %s %s" % (space * indent , "transform", ""))
                act_inst.append("%s %s %s" % (space * indent , "steps", 5))
                act_inst.append("%s %s %s" % (space * indent , "times", "0 1"))                
                for exh in range(ln):
                    act_inst.append("%s %s %s" % (space * indent , "row", ' '.join(inst['trans'][exh])))                
            act_inst.append("%s %s %s" % (space * indent , "shader", "Material.shader"))
            indent -= 1 
            act_inst.append("%s %s %s" % (space * indent , "}", ""))
            # act_inst.append("%s %s %s" % (space * indent , "modifier", " "))
    instfile = open("E:\Graphics\Works\\testbuildsfor253\DupliesTest\Objects.ins.sc" , 'w')
    for x in act_inst:
        instfile.write("\n%s" % x)
    instfile.close()



if __name__ == '__main__':
    pass