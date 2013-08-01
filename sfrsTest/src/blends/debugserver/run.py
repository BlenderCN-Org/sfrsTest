'''
Created on 01-Aug-2013
@author: AppleCart
'''
#script to run:
SCRIPT = "E:\\DevelProjects\\gitRepository\\sfrsTest\\sfrsTest\\src\\sfrsMinimal\\runthisscript.py"  
    
#path to your org.python.pydev.debug* folder (it may have different version number, in your configuration):
PYDEVD_PATH='E:\\Eclipse\\plugins\\org.python.pydev_2.7.1.2012100913\\pysrc'

import pydev_debug as pydev

pydev.debug(SCRIPT, PYDEVD_PATH, trace=True)
