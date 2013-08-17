'''
Created on 16-Aug-2013
@author: AppleCart
'''

filepath = r'E:\DevelProjects\EclipseWS\Experimental\src\Dictionary\outfolder\Instances.blend'
scenename = 'Scene'
framenumber = 1
dictionary = {
        'trace':
        {'trace': [' trace-depths {', '         diff 1', '         refl 4', '         refr 4', '         } ']}
        ,
        'ExportedObjects':
            {
             'Suzanne': {'is_dupli': False, 'modifiers': [], 'parent': 'Suzanne', 'trans_mat': [['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '-0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '-0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '-0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '-0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '-0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000']], 'materials': ['Material.002'], 'objectfile': 'c:\\users\\applec~1\\appdata\\local\\temp\\tmpk22rav.Suzanne.sc'},
             'Cube': {'is_dupli': False, 'modifiers': [], 'parent': 'Cube', 'trans_mat': [['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000'], ['+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000', '+0.0000', '+0.0000', '+0.0000', '+0.0000', '+1.0000']], 'materials': ['Material.001', 'Material.004'], 'objectfile': 'c:\\users\\applec~1\\appdata\\local\\temp\\tmp9ii51s.Cube.sc'},
             'Sphere': {'is_dupli': False, 'modifiers': [], 'parent': 'Sphere', 'trans_mat': [], 'materials': ['Material'], 'objectfile': 'c:\\users\\applec~1\\appdata\\local\\temp\\tmpd6ykoj.Sphere.sc'}
             }
        ,
        'output':
        {'output': [' image {', '         resolution 960.00  540.00', '         aa 0  1', '         samples 4', '         filter mitchell', '         jitter False', '         } ']}
        ,
        'Instances':
        {}
        ,
        'Shadermodifier':
        {'Material.001': [' modifier {', '         name  "Material.001"', '         type bump', '         texture  "E:\\DevelProjects\\gitRepository\\sfrsTest\\sfrsTest\\src\\blends\\casestudies\\outputCycle.png"', '         scale +1.0000', '         } ']}
        ,
        'MeshLightObjects':
        {}
        ,
        'cmd':
        {'smallmesh': '-smallmesh', 'verbosity': '', 'quick': '', 'threads': '', 'threadprio': ''}
        ,
        'background':
        {'background': [' background {', '         color {', '                 "sRGB nonlinear" +0.0509  +0.0509  +0.0509', '                 } ', '         } ']}
        ,
        'MotionBlurObjects':
        {'Suzanne': True, 'Cube': True}
        ,
        'lamp':
        {'Lamp': [' light  {', '         type   point', '         color    {', '                 "sRGB nonlinear" +1.0000  +1.0000  +1.0000', '                 } ', '         power +10.0000', '         p     +4.0762 +1.0055 +5.9039', '         } ']}
        ,
        'bucket':
        {'bucket': [' bucket 64 hilbert']}
        ,
        'world':
        {}
        ,
        'caustics':
        {}
        ,
        'Instantiated':
        {}
        ,
        'Camera':
        {'Camera': [' camera {', '         type pinhole', '         shutter 0 1', '         eye    +0.0000 +0.0000 +20.0000', '         target +0.0000 +0.0000 +19.0000', '         up     +0.0000 +1.0000 +0.0000', '         fov    49.13434', '         aspect 1.77778', '         } ']}
        ,
        'Shaderlight':
        {'Material': ['         emit   {', '                 "sRGB nonlinear" +0.8000  +0.8000  +0.8000', '                 } ', '         radiance +10.0000', '         samples  16']}
        ,
        'Shader':
        {'Material.004': [' shader {', '         name "Material.004"', '         type diffuse', '         color   {', '                 "sRGB nonlinear" +0.0202  +0.2800  +0.8000', '                 } ', '         } '], 'Material.002': [' shader {', '         name "Material.002"', '         type diffuse', '         color   {', '                 "sRGB nonlinear" +0.8000  +0.8000  +0.8000', '                 } ', '         } '], 'Material.003': [' shader {', '         name "Material.003"', '         type diffuse', '         color   {', '                 "sRGB nonlinear" +0.8000  +0.8000  +0.8000', '                 } ', '         } '], 'Material.001': [' shader {', '         name "Material.001"', '         type shiny', '         diff   {', '                 "sRGB nonlinear" +0.8000  +0.8000  +0.8000', '                 } ', '         refl   +0.0100', '         } ']}
        ,
        'gi':
        {}
        ,
}


import os

class Assemble():
    
    def __init__(self, dictionary, filepath, scenename, framenumber):
        self._di = dictionary
        self._sn = scenename
        self._fn = framenumber
        self._fp = filepath
        self._dp = None
        self._fh = None
        self._name = None
        self._includes = set()
        self._inclf = None
        self._objlist = []



    
    def write_output_block(self, int_blk=[], def_block=[], fnl_blk=[], filename="", def_block_file=True):
        pushout = open(filename , 'a')
        for lines in int_blk:
            pushout.write("\n%s" % lines)
        if def_block_file:
            for lines in def_block:
                pushout.write("%s" % lines)
        else:
            for lines in def_block:
                pushout.write("\n%s" % lines)
        for lines in fnl_blk:
            pushout.write("\n%s" % lines)
        pushout.close()
    
    
    def writable(self, filename):
        try:
            pushout = open(filename , 'a')
            pushout.close()
            return True
        except:
            return False
    
    
    def compileObjectBlocks(self):
        for objs in self._objlist:
            # print(objs)
            main_file, sub_file = objs
            if sub_file in self._di['MeshLightObjects'].keys():
                self.compileObjectBlocksLight(objs)
                continue
            if sub_file in self._di['ExportedObjects'].keys():
                self.compileObjectBlocksNormal(objs)
                continue
                


    def makeFileName(self):
        self._name = ("%s.%03d" % (self._sn , self._fn))
        self._inclf = os.path.join(self._dp , "_include." + self._name)
        if not os.path.exists(self._inclf):
            os.makedirs(self._inclf)
        
        
    
    
    
    def compileLightsBlock(self):
        key = 'lamp'
        if key not in self._di.keys():
            return
        for ekey in self._di[key].keys():
            block = self._di[key][ekey]
            self.write_output_block(block, [""] , [] , self._fh, False)
    
    
    def compileCameraBlock(self):
        key = 'Camera'
        if key not in self._di.keys():
            return
        for ekey in self._di[key].keys():
            block = self._di[key][ekey]
            self.write_output_block(block, [""] , [] , self._fh, False)
    
    
    def compileIncludes(self):
        self._includes
        inclu = [(files[-6:], files) for files in self._includes]
        inclu.sort()
        block = []
        for inc in inclu:
            name = ' "%s%s\%s"' % ("_include." , self._name, inc[1])
            block.append("%s %s %s" % ("include" , "", name))
        self.write_output_block(block, [""] , [] , self._fh, False)
    
    
    def compileMainBlock(self):
        self._name = ("%s.%03d" % (self._sn , self._fn))
        self._fh = os.path.join(self._dp , "%s.sc" % self._name)
        if not os.path.exists(self._fh):
            self.writable(self._fh)
        else:
            os.remove(self._fh)
        
        key_list = ['output', 'trace' , 'background' , 'bucket' , 'caustics' , 'gi']

        for key in key_list:
            if key not in self._di.keys():
                continue
            if key not in self._di[key].keys():
                continue
            block = self._di[key][key]
            self.write_output_block(block, [""] , [] , self._fh, False)
         
        self.comipleShaderBlock()
        self.compileLightsBlock()
        self.compileCameraBlock()
        self.compileIncludes()
    
    def comipleShaderBlock(self):
        shader = self._di['Shader'].keys()
        for each_shader in shader:
            block = self._di['Shader'][each_shader]
            self.write_output_block(block, [""] , [] , self._fh, False)
    
    
    def createObjectFiles(self):
        if not self.getFolderPath():
            return "Failed"
        self.populate_MeshLightObjects()
        self.populate_modifiers()
        self.getObjectsList()
        self.makeFileName()
        self.cleanFolder()
        self.compileObjectBlocks()
        self.compileInstanceBlocks()
        self.compileMainBlock()
        
        
        
        
        
    def getFolderPath(self):
        self._dp , self._ne = os.path.split(self._fp)
        self._dp = os.path.abspath(self._dp)
        self._ne = self._ne.split('.')[:-1]
        return os.path.exists(self._dp)        
        
    
    def populate_MeshLightObjects(self):
        
        light_mat = self._di['Shaderlight'].keys()
        if len(light_mat) <= 0:
            return
        exported = self._di['ExportedObjects']
        
        for obj in exported.keys():
            expmat = exported[obj]['materials']
            found = { mat:index for index, mat in enumerate(light_mat) if mat in expmat}
            if len(found) > 0:
                self._di['MeshLightObjects'][exported[obj]['parent']] = found
        
        
    def populate_modifiers(self):
        
        mod_mat = self._di['Shadermodifier'].keys()
        exported = self._di['ExportedObjects']
        for obj in exported.keys():
            expmat = exported[obj]['materials']
            mod_list = []
            for mat in expmat:
                if mat in mod_mat:
                    mod_list.append(mat)
                else:
                    mod_list.append("None")
            exported[obj]['modifiers'] = mod_list[:]
            
            
    def consoleprintdict(self):           
        print("{")
        for keys in self._di.keys():
            print("'%s':" % keys)
            print(self._di[keys])
            print(",")
        print("}")
        
    def consoleprintobjects(self):
        for keys in self._di['ExportedObjects'].values():
            print(keys)

    def getObjectsList(self):
        obj = []
        for keys in self._di['ExportedObjects'].keys():
            obj.append((self._di['ExportedObjects'][keys]['parent'] , keys))
        obj.sort()
        self._objlist = obj[:]
        
    def cleanFolder(self):
        for obj in self._objlist:
            filename = os.path.join(self._inclf , "%s.geo.sc" % (obj[0]))
            if os.path.exists(filename):
                os.remove(filename)
            filename = os.path.join(self._inclf , "%s.ins.sc" % (obj[0]))
            if os.path.exists(filename):
                os.remove(filename)


    def compileInstanceBlocks(self):
        for instancess in self._di['Instantiated'].keys():
            ins_names = [ instblock for instblock in self._di['Instances'].keys() if instblock.split('.')[0] == instancess]
            for each_inst in ins_names:
                act_inst = []
                indent = 0
                space = "        "
                
                 
                ins = self._di['Instances'][each_inst]
                # print(ins)
                original_obj = ins['pname']
                int_blk = []  


                if original_obj in self._di['ExportedObjects'].keys():
                    block_dirct = self._di['ExportedObjects'][original_obj]                    
                    indent += 1 
                    num_of_shaders = len(block_dirct['materials'])
                    if  num_of_shaders > 1:
                        int_blk.append("%s %s %s" % (space * indent , "shaders", num_of_shaders))
                        indent += 1
                        for each_shdr in block_dirct['materials']:
                            int_blk.append("%s %s %s" % (space * indent , "", each_shdr))
                        indent -= 1
                    else:
                        int_blk.append("%s %s %s" % (space * indent , "shader", block_dirct['materials'][0]))
                     
                     
                    num_of_shaders = len(block_dirct['modifiers'])
                    if  num_of_shaders > 1:
                        int_blk.append("%s %s %s" % (space * indent , "modifiers", num_of_shaders))
                        indent += 1
                        for each_shdr in block_dirct['modifiers']:
                            int_blk.append("%s %s %s" % (space * indent , "", each_shdr))
                        indent -= 1
                    else:
                        int_blk.append("%s %s %s" % (space * indent , "modifier", block_dirct['modifiers'][0]))
                    indent -= 1
                     

                act_inst.append("%s %s %s" % (space * indent , "instance", "{"))
                indent += 1 
                act_inst.append("%s %s %s" % (space * indent , "name", ins['iname']))
                act_inst.append("%s %s %s" % (space * indent , "geometry", ins['pname']))
                ln = len(ins['trans'])
                if ln == 1:
                    act_inst.append("%s %s %s" % (space * indent , "transform  row", ' '.join(ins['trans'][0])))
                else:
                    act_inst.append("%s %s %s" % (space * indent , "transform", ""))
                    act_inst.append("%s %s %s" % (space * indent , "steps", ln))
                    act_inst.append("%s %s %s" % (space * indent , "times", " 0.0 1.0"))                
                    for exh in range(ln):
                        act_inst.append("%s %s %s" % (space * indent , "row", ' '.join(ins['trans'][exh]))) 
                act_inst.extend(int_blk)
                indent -= 1 
                act_inst.append("%s %s %s" % (space * indent , "}", ""))
                
                fname = "%s.ins.sc" % instancess
                filename = os.path.join(self._inclf , fname)
                if not self.writable(filename):
                    return
                self.write_output_block(act_inst, [], [], filename, False)        
                self._includes.add(fname)
                
    

    def compileObjectBlocksNormal(self, objs):
        main_file, sub_file = objs
        block_dirct = self._di['ExportedObjects'][sub_file]
        int_blk = [] 
        indent = 0
        space = "        "
        
        int_blk.append("%s %s %s" % (space * indent , "object", "{"))
        indent += 1
        num_of_shaders = len(block_dirct['materials'])
        if  num_of_shaders > 1:
            int_blk.append("%s %s %s" % (space * indent , "shaders", num_of_shaders))
            indent += 1
            for each_shdr in block_dirct['materials']:
                int_blk.append("%s %s %s" % (space * indent , "", each_shdr))
            indent -= 1
        else:
            int_blk.append("%s %s %s" % (space * indent , "shader", block_dirct['materials'][0]))
        
        
        num_of_shaders = len(block_dirct['modifiers'])
        if  num_of_shaders > 1:
            int_blk.append("%s %s %s" % (space * indent , "modifiers", num_of_shaders))
            indent += 1
            for each_shdr in block_dirct['modifiers']:
                int_blk.append("%s %s %s" % (space * indent , "", each_shdr))
            indent -= 1
        else:
            int_blk.append("%s %s %s" % (space * indent , "modifier", block_dirct['modifiers'][0]))
        
        num_of_transforms = len(block_dirct['trans_mat']) 
        if num_of_transforms > 0 :
            int_blk.append("%s %s %s" % (space * indent , "transform", ""))
            int_blk.append("%s %s %s" % (space * indent , "steps ", num_of_transforms))
            int_blk.append("%s %s %s" % (space * indent , "times", " 0.0 1.0"))
            indent += 1
            for each_trn in block_dirct['trans_mat']:
                int_blk.append("%s %s %s" % (space * indent , "row", ' '.join(each_trn)))
            indent -= 1
        int_blk.append("%s %s %s" % (space * indent , "type", "generic-mesh"))
        int_blk.append("%s %s %s" % (space * indent , "name", sub_file))
        
        fnl_blk = []
        fnl_blk.append("%s %s %s" % (space * indent , "}", ""))
        
        def_block = block_dirct['objectfile']
        if not os.path.exists(def_block):
            return
        def_block_handle = open(def_block , 'r')
        fname = "%s.geo.sc" % main_file
        filename = os.path.join(self._inclf , fname)
        if not self.writable(filename):
            return
        self.write_output_block(int_blk, def_block_handle, fnl_blk, filename, True)        
        self._includes.add(fname)

    
  
    def compileObjectBlocksLight(self, objs):        
        main_file, sub_file = objs
        block_dirct = self._di['ExportedObjects'][sub_file]
        int_blk = [] 
        indent = 0
        space = "        "
        
        int_blk.append("%s %s %s" % (space * indent , "light", "{"))
        indent += 1
        
        int_blk.append("%s %s %s" % (space * indent , "type", "meshlight"))
        int_blk.append("%s %s %s" % (space * indent , "name", sub_file))
        
        mat = self._di['MeshLightObjects'][sub_file].keys()[0]
        desc = self._di['Shaderlight'][mat]
        
        int_blk.extend(desc)
        
        fnl_blk = []
        fnl_blk.append("%s %s %s" % (space * indent , "}", ""))
        
        def_block = block_dirct['objectfile']
        if not os.path.exists(def_block):
            return
        def_block_handle = open(def_block , 'r')
        datablock = []
        for eachline in def_block_handle:
            splt = eachline.split()
            if (('normals' in splt) | ('uvs' in splt) | ('face_shaders' in splt)):
                break
            datablock.append(eachline)
        
        fname = "%s.geo.sc" % main_file
        filename = os.path.join(self._inclf , fname)
        if not self.writable(filename):
            return
        self.write_output_block(int_blk, datablock, fnl_blk, filename, False)        
        self._includes.add(fname)
    
    # TODO: need to fill mesh light block


def testmod():
    ass = Assemble(dictionary, filepath, scenename, framenumber)
    ass.createObjectFiles()












if __name__ == '__main__':
    testmod()
