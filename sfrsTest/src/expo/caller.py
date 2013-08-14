'''
Created on 14-Aug-2013

@author: AppleCart
'''

import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from pack import main 


main.getExporter()